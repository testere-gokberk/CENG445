# server.py

import json
from websockets.sync.server import serve  
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
import threading
from threading import Lock
from components import Cell, Car
from repo import Repo


class MapServer:
    def __init__(self, host="127.0.0.1", port=1423):
        self.host = host
        self.port = port
        self.repo = Repo()
        self.lock = Lock()
        self.clients = []  # List of (username, websocket) tuples
        print(f"Server starting on {self.host}:{self.port}")

    def notify_users_on_map(self, users, message):
        threads = []
        for user, wsock in self.clients:
            if user in users:
                thread = threading.Thread(target=self.send_message, args=(wsock, message))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

    def send_message(self, wsock, message):
        try:
            wsock.send(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")

    def handle_client(self, wsock):
        username = None
        try:
            wsock.send(json.dumps({
                "status": "request",
                "message": "Enter username:"
            }))

            msg = wsock.recv()
            try:
                data = json.loads(msg)
                username = data.get("username", "").strip()
            except json.JSONDecodeError:
                username = msg.strip()  

            if not username:
                wsock.send(json.dumps({
                    "status": "error",
                    "message": "Invalid username. Connection closing."
                }))
                return

            print(f"User connected: {username}")


            if username in self.repo.users:
                wsock.send(json.dumps({
                    "status": "success",
                    "message": f"Welcome back, {username}! You can enter your commands now."
                }))
            else:
                self.repo.users[username] = []
                wsock.send(json.dumps({
                    "status": "success",
                    "message": f"Welcome, {username}! You can enter your commands now."
                }))

            self.clients.append((username, wsock))

            while True:
                msg = wsock.recv()
                try:
                    data = json.loads(msg)
                    command = data.get("command")
                    params = data.get("params", [])
                except json.JSONDecodeError:
                    parts = msg.strip().split()
                    command = parts[0] if parts else ""
                    params = parts[1:] if len(parts) > 1 else []

                response = self.process_request(command, params, username)
                wsock.send(json.dumps(response))

        except ConnectionClosedOK:
            print(f"Connection closed normally by {username}")
        except ConnectionClosedError as e:
            print(f"Connection error with {username}: {e}")
        except Exception as e:
            print(f"Error handling client {username}: {e}")
        finally:
            if username:
                self.clients = [client for client in self.clients if client[0] != username]
            print(f"Connection closed with {username}")


    def process_request(self, command, params, username):
        try:
            with self.lock:
                attached_maps = self.repo.listattached(username) if username in self.repo.users else []
                if attached_maps:
                    
                    attached_map_id = attached_maps[0]
                    map_object = self.repo.objects[attached_map_id]

                    if map_object.game_active and (command != "stop" or command != "left" or command != "right" or command != "accel" or command != "break_"):
                        return {"status": "error", "message": "First stop the game mode."}

                if command == "left":

                    map = self.repo.objects[attached_map_id]

                    for objs in map.objects:
                        if isinstance(objs, Car):
                            if (objs.driver == username):
                                objs.left()
                                break
                    return {"status": "success", "message": f"Car {objs.id} turned left"}

                elif command == "right":
                    map = self.repo.objects[attached_map_id]
                    for objs in map.objects:
                        if isinstance(objs, Car):
                            if (objs.driver == username):
                                objs.right()
                                break
                    return {"status": "success", "message": f"Car {objs.id} turned right"}

                elif command == "accel":
                    map = self.repo.objects[attached_map_id]
                    for objs in map.objects:
                        if isinstance(objs, Car):
                            if (objs.driver == username):
                                objs.accel()
                                break
                    return {"status": "success", "message": f"Car {objs.id} accelerated"}

                elif command == "break_":
                    map = self.repo.objects[attached_map_id]
                    for objs in map.objects:
                        if isinstance(objs, Car):
                            if (objs.driver == username):
                                objs.accel()
                                break
                    return {"status": "success", "message": f"Car {objs.id} breaked"}

                elif command == "create_map":
                    if len(params) != 5:
                        return {"status": "error",
                                "message": "Invalid parameters. Usage: create_map <id:int> <cols:int> <rows:int> <cellsize:int> <bgcolor:str>"}

                    map_id = int(params[0])
                    cols = int(params[1])
                    rows = int(params[2])
                    cellsize = int(params[3])
                    bgcolor = params[4]

                    affected_users = [user for user, _ in self.clients]
                    notify_msg = f"Map {map_id} created with {cols} {rows} {cellsize} {bgcolor}."
                    ##self.notify_users_on_map(affected_users, notify_msg)

                    self.repo.create(map_id, cols, rows, cellsize, bgcolor)
                    return {"status": "success", "message": f"Map {map_id} created with {cols} {rows} {cellsize} {bgcolor}."}

                elif command == "create":
                    try:
                        attached_map_id = self.repo.listattached(username)[-1]
                    except:
                        return {"status": "error", "message": "First attach a map"}


                    map = self.repo.objects[attached_map_id]
                    component_type = params[0]

                    if component_type == 'Ferrari' or component_type == 'Merso':
                        for objs in map.objects:
                            if isinstance(objs, Car):
                                if (objs.driver == username):
                                    return {"status": "error",
                                            "message": f"You are already driving car : {objs.id}"}

                    rows = int(params[1])
                    cols = int(params[2])
                    x = rows * map.cellsize + map.cellsize / 2
                    y = cols * map.cellsize + map.cellsize / 2

                    try:
                        new_component = map.components.create(component_type)
                        if component_type == 'Ferrari' or component_type == 'Merso':
                            new_component.driver = username
                            new_component.pos = (x, y)
                        component_id = new_component.id

                        users_on_same_map = [
                            user for user, maps in self.repo.users.items()
                            if maps and maps[-1] == attached_map_id
                        ]
                        
                        ##notify_msg = f"New component of type '{component_type}' created on map {attached_map_id} with ID: {component_id}"
                        ##self.notify_users_on_map(users_on_same_map, notify_msg)

                        return {"status": "success",
                                "message": str(new_component.id),
                                "component_id": new_component.id}

                    except Exception as e:
                        return {"status": "error", "message": str(e)}

                elif command == "place":
                    try:
                        attached_map_id = self.repo.listattached(username)[-1]
                    except:
                        return {"status": "error", "message": "First attach a map"}

                    if len(params) != 3:
                        return {"status": "error",
                                "message": "Invalid parameters. Usage: place <component_id> <row> <col>"}

                    try:
                        component_id = int(params[0])
                        row = int(params[1])
                        col = int(params[2])
                    except ValueError:
                        return {"status": "error", "message": "Invalid parameter types"}

                    map = self.repo.objects[attached_map_id]
                    comp = None

                    for objs in map.objects:
                        if objs.id == component_id:
                            comp = objs
                            break

                    rowcount = map.rows
                    colcount = map.cols
                    if not (0 <= row < rowcount and 0 <= col < colcount):
                        return {"status": "error",
                                "message": f"Invalid position. Row must be between 0 and {rowcount - 1}, col between 0 and {colcount - 1}"}

                    map[(row, col)] = comp
                    
                    users_on_same_map = [
                        user for user, maps in self.repo.users.items()
                        if maps and maps[-1] == attached_map_id
                    ]
                    
                    notify_msg = {"status": "notification", "message": f"Component '{component_id}' placed at ({row}, {col}) on map {attached_map_id}", "component_id" : component_id,"row" : row, "col" : col}
                    self.notify_users_on_map(users_on_same_map, notify_msg)

                    return {"status": "success", "message": f"Component '{component_id}' placed at ({row}, {col}) on map {attached_map_id}"}

                elif command == "rotate":
                    if len(params) != 2:
                        return {"status": "error",
                                "message": "Invalid parameters. Usage: rotate <cell_id> <map_id>"}

                    try:
                        cell_id = int(params[0])
                        map_id = int(params[1])
                    except ValueError:
                        return {"status": "error", "message": "Invalid parameter types"}

                    map = self.repo.objects[map_id]
                    cell = None

                    for objs in map.objects:
                        if cell_id == objs.id:
                            cell = objs
                            break
                    if cell == None:
                        return {"status": "error", "message": f"Cell with ID '{cell_id}' not found."}

                    if not hasattr(cell, "rotation"):
                        return {"status": "error", "message": "Only cells can be rotated"}

                    cell.rotation = (cell.rotation + 1) % 4

                    attached_map_id = self.repo.listattached(username)[0]
                    
                    users_on_same_map = [
                        user for user, maps in self.repo.users.items()
                        if maps and maps[-1] == attached_map_id
                    ]

                    
                    notify_msg = {"status": "notification","message":f"Component '{cell_id}' rotated. New rotation: {cell.rotation}"}
                    self.notify_users_on_map(users_on_same_map, notify_msg)

                    return {"status": "success", "message": f"Component '{cell_id}' rotated. New rotation: {cell.rotation}"}

                elif command == "attach":
                    if len(params) != 1:
                        return {"status": "error",
                                "message": "Invalid parameters. Usage: attach <map_id>"}

                    try:
                        map_id = int(params[0])
                        obj = self.repo.attach(map_id, username)

                        comps = {}
                        for objs in obj.objects:
                            if isinstance(objs, Cell):
                                comps[objs.id] = [objs.row, objs.col, objs.rotation, objs.tip]
                            elif isinstance(objs, Car):
                                comps[objs.id] = [objs.pos[0] / obj.cellsize,
                                                  objs.pos[1] / obj.cellsize,
                                                  objs.angle / 90,
                                                  objs.tip]

                        return {"status": "success", "components": comps}

                    except ValueError as e:
                        return {"status": "error", "message": str(e)}

                elif command == "detach":
                    if len(params) != 1:
                        return {"status": "error",
                                "message": "Invalid parameters. Usage: detach <map_id>"}

                    map_id = int(params[0])
                    self.repo.detach(map_id, username)
                    return {"status": "success",
                            "message": f"Object {map_id} detached from user {username}"}

                elif command == "game_mode":
                    attached_maps = self.repo.listattached(username)
                    if not attached_maps:
                        return {"status": "error",
                                "message": "You must attach to a map first"}

                    attached_map_id = attached_maps[-1]
                    
                    users_on_same_map = [
                        user for user, maps in self.repo.users.items()
                        if maps and maps[-1] == attached_map_id
                    ]
                    
                    
                    notify_msg = {"status": "notification", "message":f"{username} started game mode on map {attached_map_id}"}
                    self.notify_users_on_map(users_on_same_map, notify_msg)

                    map = self.repo.objects[attached_map_id]
                    map.server = self

                    def start_game_mode():
                        try:
                            map.start(users_on_same_map,attached_map_id)
                        except Exception as e:
                            print(f"Error in game mode for map {attached_map_id}: {e}")

                    game_thread = threading.Thread(target=start_game_mode, daemon=True)
                    game_thread.start()

                    return {"status": "success",
                            "message": f"Game mode started on map {attached_map_id}"}

                elif command == "stop":
                    attached_maps = self.repo.listattached(username)
                    if not attached_maps:
                        return {"status": "error", "message": "You must attach to a map first"}

                    attached_map_id = attached_maps[-1]
                    map = self.repo.objects[attached_map_id]
                    map.game_active = False

                    users_on_same_map = [
                        user for user, maps in self.repo.users.items()
                        if maps and maps[-1] == attached_map_id
                    ]
                    
                    
                    notify_msg = {"status": "notification",
                                  "message": f"{username} stopped game mode on map {attached_map_id}"}
                    self.notify_users_on_map(users_on_same_map, notify_msg)

                    return {"status": "success", "message": f"Game mode stopped on map {attached_map_id}"}

                elif command == "list_maps":
                    if len(params) != 0:
                        return "Invalid command. Correct usage: list_maps (no arguments required)\n"

                    maps = list(self.repo.objects.keys())
                    print(maps)
                    return {"status": "success","message" : f"maps has been listed","maps" : maps}

                elif command == "delete":
                    try:
                        if len(params) != 2:
                            return {"status": "error", "message": "Invalid parameter types"}

                        if params[0] == "object":
                            try:
                                if not params[1].isdigit():
                                    return f"Error: '{params[1]}' is not a valid integer. Please provide a valid ID.\n"

                                obj_id = int(params[1])
                                try:
                                    if obj_id not in self.repo.objects:
                                        return f"Object with ID {obj_id} does not exist.\n"
                                    obj = self.repo.objects[obj_id]

                                except KeyError:
                                    return f"Object with ID {obj_id} does not exist.\n"

                                a = len(self.repo.objowners[obj_id])

                                if len(self.repo.objowners[obj_id]) != 0:
                                    return f"object attached to someone\n"

                                affected_users = [user for _, user in self.clients]
                                message = f"Object {obj_id} has been deleted.\n"
                                self.notify_users_on_map(affected_users, message)

                                self.repo.delete(obj_id)

                                return f"Object with ID {obj_id} deleted successfully.\n"
                            except KeyError as e:
                                return f"Error: {e}.\n"

                        elif params[0] == "component":
                            try:
                                attached_map_id = self.repo.listattached(username)[-1]
                            except:
                                return {"status": "error", "message": "first attach a map"}
                            try:
                                obj_id = int(params[1])

                                map = self.repo.objects[attached_map_id]

                                if obj_id in [o.id for o in map.objects]:

                                    message = {"status": "notification", "message": f"{username} has deleted Component {obj_id}."}

                                    users_on_same_map = [
                                        user for user, maps in self.repo.users.items()
                                        if maps and maps[-1] == attached_map_id
                                    ]

                                    
                                    self.notify_users_on_map(users_on_same_map, message)

                                    for o in map.objects:
                                        if o.id == obj_id:
                                            map.objects.remove(o)
                                            break

                                    map.delobj(obj_id)
                                    return {"status": "success", "message": f"Component with ID {obj_id} deleted successfully."}

                                else:
                                    return {"status": "error", "message": f"Error: Component with ID {obj_id} not found."}

                            except ValueError:
                                return {"status": "error",
                                        "message": f"Error: ID must be an integer for component."}

                        else:
                            return {"status": "error",
                                    "message": f"Error: Invalid delete type. Use 'object' or 'component'."}
                    except Exception as e:
                        return {"status": "error",
                                "message": f"Error processing request: {str(e)}"}


                elif command == "list_attached":
                    if len(params) != 0:
                        return "Invalid command. Correct usage: list_attached (no arguments required)\n"

                    attached_maps = self.repo.listattached(username) if username in self.repo.users else []

                    return f"Attached objects for {username}: {attached_maps}\n"

                elif command == "map_size":

                    obj_id = int(params[0])
                    map = self.repo.objects[obj_id]
                    x = [map.rows, map.cols, map.cellsize, map.bgcolor]
                    return {"status": "success","message" : f"map size returned","map_size" : x}
                
                elif command == "component_at":
                    
                    print("INSIDE COMPONENT AT")
                    
                    print("PARAMS ", params)
                    
                    map_id = int(params[0])
                    rows = int(params[1])
                    cols = int(params[2])
                    
                    map = self.repo.objects[map_id]

                    print("MAP ", map)

                    component_id = map.getxy(rows,cols).id
                    
                    print("COMP ID ", component_id)

                    return {"status": "success", "obj_id":component_id}

                elif command == "save":
                    return {"status": "success","message" : f"repo saved successfully"}

                else:
                    return {"status": "error", "message": "Invalid command"}

        except Exception as e:
            return {"status": "error", "message": f"Error processing request: {str(e)}"}
    def start(self):
        try:
            print("Server is running...")
            with serve(self.handle_client, self.host, self.port) as server_instance:
                server_instance.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
        except Exception as e:
            print(f"Server error: {e}")

if __name__ == "__main__":
    server = MapServer()
    server.start()