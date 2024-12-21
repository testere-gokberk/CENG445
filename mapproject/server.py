import socket
import threading
from threading import Lock

from repo import Repo

class MapServer:
    def __init__(self, host="127.0.0.1", port=1423):
        self.host = host
        self.port = port
        self.repo = Repo()
        ##self.repo.load()
        self.lock = Lock()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        self.clients = []

        print(f"Server listening on {self.host}:{self.port}\n")

    def notify_users_on_map(self, users, message):
        threads = []
        for user in users:
            conn = self.get_connection_for_user(user)
            if conn:
                thread = threading.Thread(target=self.send_message, args=(conn, message))
                threads.append(thread)
                thread.start()
        for thread in threads:
            thread.join()

    def send_message(self, conn, message):
        try:
            conn.sendall(message.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")

    def get_connection_for_user(self, username):
        for conn, user in self.clients:
            if user == username:
                return conn
        return None

    def handle_client(self, conn, addr):
        print(f"Connected by {addr}\n")
        username = None
        try:
            conn.sendall("Enter username:".encode('utf-8'))
            username = conn.recv(1024).decode('utf-8').strip()
            if not username:
                conn.sendall("Invalid username. Connection closing.\n".encode('utf-8'))
                return
            print(f"Username set for connection {addr}: {username}\n")
            if username in self.repo.users:
                conn.sendall(f"Welcome back, {username}! You can enter your commands now.\n".encode('utf-8'))
                print(f"Username {username} already exists.\n")
            else:
                print(f"Username set for connection {addr}: {username}\n")
                conn.sendall(f"Welcome, {username}! You can enter your commands now.\n".encode('utf-8'))
                self.repo.users[username] = []

            self.clients.append((conn, username))
            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    break
                response = self.process_request(data, username)
                conn.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}\n")
        finally:
            self.clients = [client for client in self.clients if client[0] != conn]
            conn.close()
            print(f"Connection with {addr} closed\n")

    def process_request(self, request, username):
        try:
            parts = request.split()
            if not parts:
                return "Invalid command. Please provide a valid command and arguments.\n"

            action = parts[0]  # The first word is the action/command
            params = parts[1:]  # Remaining parts are parameters

            with self.lock:
                attached_maps = self.repo.listattached(username) if username in self.repo.users else []
                if attached_maps:
                    attached_map_id = attached_maps[0]
                    map_object = self.repo.objects[attached_map_id]

                    # Check if the map is in game mode
                    if map_object.game_active:
                        if action != "stop":
                            return "First stop the game mode.\n"


                if action == "create_map":
                    print("map created.\n")
                    if len(params) != 5:
                        return "Invalid command or missing parameters. Correct usage: create_map <id:int> <cols:int> <rows:int> <cellsize:int> <bgcolor:str>\n"
                    print("map created.\n")
                    map_id = int(params[0])
                    cols = int(params[1])
                    rows = int(params[2])
                    cellsize = int(params[3])
                    bgcolor = params[4]
                    affected_users = [user for _, user in self.clients]

                    message = f" Map {map_id} created with {cols} {rows} {cellsize} {bgcolor}.\n"
                    self.notify_users_on_map(affected_users, message)

                    self.repo.create(map_id, cols, rows, cellsize, bgcolor)
                    print("map created.\n")
                    return "Map created successfully.\n"

                elif action == "save":
                    self.repo.save()
                    return "Repository saved successfully.\n"

                elif action == "create":
                    print("create_come")
                    try:
                        attached_map_id = self.repo.listattached(username)[0]
                    except:
                        return f"first attach a map\n"

                    if len(params) != 1:
                        return "Invalid command or missing parameters. Correct usage: create <component_type>\n"


                    map = self.repo.objects[attached_map_id]

                    component_type = params[0]

                    try:
                        component_id = self.repo.components.id_counter
                        new_component = map.components.create(component_type)
                        self.repo.component_dict[component_id] = new_component
                        self.repo.component_dict2[component_id] = [0,0,0,component_type]

                        users_on_same_map = [user for user, maps in self.repo.users.items() if attached_map_id in maps]
                        message = f"A new component of type '{component_type}' has been created on map {attached_map_id} with ID: {component_id}\n"
                        self.notify_users_on_map(users_on_same_map, message)
                        return f"{component_id}\n"

                    except Exception as e:
                        return f"Error: {e}\n"
                elif action == "list_components":
                    if params:
                        return "Invalid command. Correct usage: list_components (no arguments required)\n"

                    components = self.repo.components.list()
                    component_strings = [str(component) for component in components]

                    return f"Components: {', '.join(component_strings)}\n" if component_strings else "No components available.\n"


                elif action == "attach":
                    # Check if the user already has an attached map
                    attached_maps = self.repo.listattached(username) if username in self.repo.users else []

                    if len(attached_maps) == 1:
                        attached_map_id = attached_maps[0]
                        return f"Only one map can be attached. Already attached map {attached_map_id}\n"
                    else:
                        if len(params) != 1:
                            return "Invalid command or missing parameters. Correct usage: attach <id:int>\n"
                        else:
                            try:

                                obj_id = int(params[0])
                                obj = self.repo.attach(obj_id, username)

                                return f"{self.repo.component_dict2}"
                            except ValueError as e:
                                return f"Error: {e}\n"
                elif action == "map_size":
                    obj_id = int(params[0])
                    map =self.repo.objects[obj_id]
                    x = [map.rows, map.cols,map.cellsize,map.bgcolor]
                    return f"{x}\n"


                elif action == "detach":
                    if len(params) != 1:
                        return "Invalid command or missing parameters. Correct usage: detach <id:int>\n"

                    obj_id = int(params[0])

                    self.repo.detach(obj_id, username)
                    return f"Object {obj_id} detached from user {username}.\n"


                elif action == "rotate":

                    if len(params) != 1:
                        return "Invalid command or missing parameters. Correct usage: rotate <cell_id:int>\n"

                    try:
                        cell_id = int(params[0])
                    except ValueError:
                        return "Error: cell_id must be an integer.\n"

                    try:
                        cell = self.repo.component_dict[cell_id]
                    except KeyError:
                        return f"Error: Component '{cell_id}' does not exist.\n"

                    if not hasattr(cell, "rotation"):
                        return "Error: Only cells can be rotated.\n"

                    cell.rotation += 1
                    if cell.rotation == 4:
                        cell.rotation = 0

                    attached_map_id = self.repo.listattached(username)[0]
                    users_on_same_map = [user for user, maps in self.repo.users.items() if attached_map_id in maps]
                    message = f"Component '{cell_id}' on map {attached_map_id} has been rotated. New rotation: {cell.rotation}."
                    self.notify_users_on_map(users_on_same_map, message)

                    return f"Cell '{cell_id}' rotated successfully. New rotation: {cell.rotation}\n"


                elif action == "get":
                    try:
                        attached_map_id = self.repo.listattached(username)[0]
                    except:
                        return f"first attach a map\n"

                    if len(params) != 2:
                        return "Invalid command or missing parameters. Correct usage: get <row:int> <col:int>\n"

                    map_object = self.repo.objects[attached_map_id]

                    try:
                        row = int(params[0])
                        col = int(params[1])
                    except ValueError:
                        return "Error: row and col must be integers.\n"
                    if not (0 <= row < map_object.rows and 0 <= col < map_object.cols):
                        return f"Error: Invalid row or col. Row must be between 0 and {map_object.rows - 1}, and col between 0 and {map_object.cols - 1}.\n"
                    try:
                        cell = map_object[(row, col)]
                    except IndexError as e:
                        return f"Error: {e}\n"
                    except Exception:
                        return f"Error: No cell at position\n"
                    return f"Component at ({row}, {col}) on Map '{attached_map_id}' id: {cell.id}\n" ## return cell id here.

                elif action == "place":
                    try:
                        attached_map_id = self.repo.listattached(username)[0]
                    except:
                        return f"first attach a map\n"

                    if len(params) != 3:
                        return "Invalid command or missing parameters. Correct usage: place <component_id> <row> <col>\n"

                    try:
                        component_id = int(params[0])
                    except ValueError:
                        return "Error: component_id must be integer.\n"

                    try:
                        row = int(params[1])
                        col = int(params[2])
                    except ValueError:
                        return "Error: row and col must be integers.\n"


                    try:
                            comp =self.repo.component_dict[component_id]
                    except KeyError:
                        return f"Error: Component '{component_id}' does not exist.\n"

                    rowcount = self.repo.objects[attached_map_id].rows
                    colcount = self.repo.objects[attached_map_id].cols
                    if not (0 <= row < rowcount and 0 <= col < colcount):
                        return f"Error: Invalid row or col. Row must be between 0 and {rowcount - 1}, and col between 0 and {colcount - 1}.\n"


                    self.repo.objects[attached_map_id][(row,col)] = comp
                    users_on_same_map = [user for user, maps in self.repo.users.items() if attached_map_id in maps]
                    message = f"Component '{component_id}' has been placed at ({row}, {col}) on map {attached_map_id}\n."
                    self.notify_users_on_map(users_on_same_map, message)

                    component_data = self.repo.component_dict2.get(component_id)
                    component_data[0] = row
                    component_data[1] = col
                    self.repo.component_dict2[component_id] = component_data

                    return f"Component '{component_id}' placed at ({row}, {col}) on the map.\n"

                elif action == "start":
                    car = self.repo.component_dict[int(params[0])]
                    car.start()
                    return f"Component '{int(params[0])}' has been started.\n"

                elif action == "tick":
                    car = self.repo.component_dict[int(params[0])]
                    car.tick()
                    return f"Component '{int(params[0])}' has been ticked.\n"
                elif action == "setspeed":
                    car = self.repo.component_dict[int(params[0])]
                    car.speed = int(params[1])
                    return f"Component '{int(params[0])}' has been set to {car.speed}.\n"


                elif action == "game_mode":
                    attached_maps = self.repo.listattached(username)
                    if not attached_maps:
                        return "You must attach to a map first before entering game mode.\n"
                    attached_map_id = attached_maps[0]
                    # Find users attached to the same map
                    users_on_same_map = [user for user, maps in self.repo.users.items() if attached_map_id in maps]
                    message = f"{username} started game mode on map {attached_map_id}.\n"
                    self.notify_users_on_map(users_on_same_map, message)
                    map = self.repo.objects[attached_map_id]
                    map.server = self
                    def start_game_mode():
                        try:
                            map.start(0.5, 2, users_on_same_map)
                        except Exception as e:
                            print(f"Error in game mode for map {attached_map_id}: {e}\n")
                    game_thread = threading.Thread(target=start_game_mode, daemon=True)
                    game_thread.start()
                    return f"You have entered game mode on map {attached_map_id}.\n"

                elif action == "stop":
                    attached_maps = self.repo.listattached(username)
                    if not attached_maps:
                        return "You must attach to a map to stop the game_mod.\n"
                    attached_map_id = attached_maps[0]
                    users_on_same_map = [user for user, maps in self.repo.users.items() if attached_map_id in maps]
                    message = f"{username} stopped game mode on map {attached_map_id}.\n"
                    self.notify_users_on_map(users_on_same_map, message)
                    map = self.repo.objects[attached_map_id]
                    map.server = self

                    map.stop()
                    return f"You have stopped game mode on map {attached_map_id}.\n"


                elif action == "delete":

                    try:
                        if len(params) != 2:
                            return "Invalid command or missing parameters. Correct usage: delete <type:str> <id:int>\n"

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
                                attached_map_id = self.repo.listattached(username)[0]
                            except:
                                return f"first attach a map\n"
                            try:
                                obj_id = int(params[1])
                                if obj_id in self.repo.component_dict:
                                    message = f"{username} has deleted Component {obj_id}.\n"

                                    users_on_same_map = [user for user, maps in self.repo.users.items() if
                                                         attached_map_id in maps]
                                    # Send a notification to all users on the same map
                                    self.notify_users_on_map(users_on_same_map, message)
                                    del self.repo.component_dict2[obj_id]
                                    del self.repo.component_dict[obj_id]
                                    return f"Component with ID {obj_id} deleted successfully.\n"
                                else:
                                    return f"Error: Component with ID {obj_id} not found.\n"


                            except ValueError:
                                return "Error: ID must be an integer for component.\n"
                        else:
                            return "Error: Invalid delete type. Use 'object' or 'component'.\n"
                    except Exception as e:
                        return f"Error processing request: {str(e)}\n"

                elif action == "list_maps":
                    if len(params) != 0:
                        return "Invalid command. Correct usage: list_maps (no arguments required)\n"

                    maps = list(self.repo.objects.keys())
                    return f"Maps: {maps}\n"

                elif action == "list_attached":
                    if len(params) != 0:
                        return "Invalid command. Correct usage: list_attached (no arguments required)\n"

                    attached_maps = self.repo.listattached(username) if username in self.repo.users else []

                    return f"Attached objects for {username}: {attached_maps}\n"


                elif action == "draw_map":
                    try:
                        attached_map_id = self.repo.listattached(username)[0]
                    except:
                        return f"first attach a map\n"
                    print(self.repo.objects[attached_map_id].cells)
                    if len(params) != 0:
                        return "Invalid command or missing parameters. Correct usage: draw_map\n"

                    if attached_map_id in self.repo.objects:
                        map_representation = self.repo.objects[attached_map_id].draw()  # Assuming `draw` returns a string now
                        return f"{map_representation}\n"
                    else:
                        return "Map ID not found.\n"

                else:
                    return "Invalid action or command.\n"
        except Exception as e:
            return f"Error processing request: {e}\n"

    def start(self):
        try:
            while True:
                conn, addr = self.server.accept()
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()
        except KeyboardInterrupt:
            print("Server shutting down...\n")
        finally:
            self.server.close()

if __name__ == "__main__":
    server = MapServer()
    server.start()
