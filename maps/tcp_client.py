import json
from websockets.sync.client import connect
from typing import Optional, Any, Dict, Union
from websockets.exceptions import WebSocketException
import threading
import queue

active_connections = {}
stop_events = {}
message_queues = {}
listener_threads = {}


def listen_for_messages(wsock, message_queue, stop_event, map_id, username):
    try:
        while not stop_event.is_set():
            try:
                server_message = wsock.recv()
                parsed_message = json.loads(server_message)

                if parsed_message.get("status") == "notification":

                    ##handle notification here
                    print(f"Notification received for map {map_id} and user {username} {parsed_message}")
                    continue

                message_queue.put(server_message)

            except WebSocketException as e:
                if not stop_event.is_set():
                    print(f"WebSocket error in listener: {e}")
                break
    except Exception as e:
        if not stop_event.is_set():
            print(f"Error in listener thread: {e}")
    finally:
        connection_key = f"{username}_{map_id}"
        if connection_key in listener_threads:
            del listener_threads[connection_key]


def maintain_connection(username: str, map_id: str) -> tuple:
    if username in active_connections:
        return (
            active_connections[username],
            message_queues[username],
            stop_events[username]
        )

    wsock = create_websocket_connection()
    if not wsock:
        raise Exception("Could not connect to server")

    initial_msg = wsock.recv()
    wsock.send(json.dumps({"username": username}))
    welcome_msg = wsock.recv()

    message_queue = queue.Queue()
    stop_event = threading.Event()

    listener_thread = threading.Thread(
        target=listen_for_messages,
        args=(wsock, message_queue, stop_event, map_id, username),
        daemon=True
    )
    listener_thread.start()

    active_connections[username] = wsock
    message_queues[username] = message_queue
    stop_events[username] = stop_event

    return wsock, message_queue, stop_event

def cleanup_connection(username: str, map_id: str):
    if username in active_connections:
        stop_events[username].set()
        active_connections[username].close()
        del active_connections[username]
        del message_queues[username]
        del stop_events[username]

def create_websocket_connection(host: str = "127.0.0.1", port: int = 1423) -> Any:
    try:
        return connect(f"ws://{host}:{port}")
    except WebSocketException as e:
        return None

def ensure_json_response(response: Optional[str]) -> str:
    if response is None:
        return json.dumps({"status": "error", "message": "No response from server"})
    try:
        json.loads(response)
        return response
    except json.JSONDecodeError:
        return json.dumps({"status": "success", "message": response})


def send_to_server(username: str, command: str, *args) -> str:
    if not username:
        return json.dumps({"status": "error", "message": "Username is required"})

    try:
        if len(args) >= 1:
            wsock, message_queue, stop_event = maintain_connection(username,
                        args[0])

        else:

            wsock, message_queue, stop_event = maintain_connection(username,
                                                                   "default")
        command_msg = {
            "command": command.lower().replace(" ", "_"),
            "params": list(args)
        }
        wsock.send(json.dumps(command_msg))
        response = message_queue.get()

        return ensure_json_response(response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Communication error: {str(e)}"
        })

def send_listmaps_to_server(username: str, command: str, *args) -> str:
    if not username:
        return json.dumps({"status": "error", "message": "Username is required"})

    try:
        # Create a new independent connection
        wsock = create_websocket_connection()
        if not wsock:
            return json.dumps({"status": "error", "message": "Could not connect to server"})

        try:
            initial_msg = wsock.recv()
            wsock.send(json.dumps({"username": "temporary"}))
            welcome_msg = wsock.recv()

            command_msg = {
                "command": command.lower().replace(" ", "_"),
                "params": list(args)
            }
            wsock.send(json.dumps(command_msg))
            response = wsock.recv()

            return ensure_json_response(response)

        finally:
            # Always close this independent connection
            wsock.close()

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Communication error: {str(e)}"
        })


def send_component_to_server(username: str, map_id: str, component: str, row: str, col: str) -> str:
    if not map_id:
        return json.dumps({"status": "error", "message": "No map attached"})

    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        attach_command = {
            "command": "attach",
            "params": [map_id]
        }
        wsock.send(json.dumps(attach_command))
        attach_response = message_queue.get()

        create_command = {
            "command": "create",
            "params": [component, row, col]
        }
        wsock.send(json.dumps(create_command))
        create_response = json.loads(message_queue.get())

        try:
            component_id = create_response.get("component_id")
            print("AŞALALLAL ", create_response)
            if not component_id and component_id != 0:
                return json.dumps({"status": "error", "message": "Failed to create component"})
        except KeyError:
            return json.dumps({"status": "error", "message": "Invalid server response"})

        place_command = {
            "command": "place",
            "params": [str(component_id), row, col]
        }
        wsock.send(json.dumps(place_command))
        place_response = json.loads(message_queue.get())

        detach_command = {
            "command": "detach",
            "params": [map_id]
        }
        wsock.send(json.dumps(detach_command))
        detach_response = message_queue.get()

        return ensure_json_response(json.dumps(create_response))#create_response# ensure_json_response(json.dumps(place_response))

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })


def send_command_to_server(username: str, command: str, *args) -> str:
    if not username:
        return json.dumps({"status": "error", "message": "Username is required"})

    try:
        wsock, message_queue, stop_event = maintain_connection(username, args[0] if args else "default")

        command_msg = {
            "command": command.lower().replace(" ", "_"),
            "params": list(args)
        }
        wsock.send(json.dumps(command_msg))
        response = message_queue.get()

        return ensure_json_response(response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Communication error: {str(e)}"
        })

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Communication error: {str(e)}"
        })



def send_delete_to_server(username: str, map_id: str, command: str, *args) -> str:
    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        attach_command = {
            "command": "attach",
            "params": [map_id]
        }
        wsock.send(json.dumps(attach_command))
        attach_response = message_queue.get()

        print("ATTECH IN DELETE ", attach_response)
    
        delete_command = {
            "command": command.lower().replace(" ", "_"),
            "params": list(args)
        }
        wsock.send(json.dumps(delete_command))
        delete_response = message_queue.get()

        print("DELETE RESPONS  IN DELETE ", delete_response)

        detach_command = {
            "command": "detach",
            "params": [map_id]
        }
        wsock.send(json.dumps(detach_command))
        detach_response = message_queue.get()
        
        print("detach_response IN DELETE ", detach_response)

        return ensure_json_response(delete_response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })

def send_rotate_to_server(username: str, map_id: str, command: str, *args) -> str:
    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        attach_command = {
            "command": "attach",
            "params": [map_id]
        }
        
        wsock.send(json.dumps(attach_command))
        attach_response = message_queue.get()

        rotate_args = list(args) + [map_id]
        rotate_command = {
            "command": command.lower().replace(" ", "_"),
            "params": rotate_args
        }
        wsock.send(json.dumps(rotate_command))
        rotate_response = message_queue.get()

        detach_command = {
            "command": "detach",
            "params": [map_id]
        }
        wsock.send(json.dumps(detach_command))
        detach_response = message_queue.get()

        return ensure_json_response(rotate_response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })


def send_gamemode_to_server(username: str, map_id: str,command:str) -> str:
    if not username:
        return json.dumps({"status": "error", "message": "Username is required"})

    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        attach_command = {
            "command": "attach",
            "params": [map_id]
        }
        wsock.send(json.dumps(attach_command))
        attach_response = message_queue.get()

        game_command = {
            "command": command,
            "params": []
        }
        wsock.send(json.dumps(game_command))
        initial_response = message_queue.get()
        def process_notifications():
            try:
                while not stop_event.is_set():
                    try:
                        notification = json.loads(message_queue.get(timeout=1))

                        if notification.get("status") == "notification":
                            # Handle the notification here
                            print(f"Game notification received: {notification}")

                    except queue.Empty:
                        continue
                    except json.JSONDecodeError:
                        print("Invalid JSON in notification")
                        continue
                    except Exception as e:
                        print(f"Error processing notification: {e}")
                        continue

            except Exception as e:
                if not stop_event.is_set():
                    print(f"Error in notification processor: {e}")

        notification_thread = threading.Thread(
            target=process_notifications,
            daemon=True
        )
        notification_thread.start()

        return ensure_json_response(initial_response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })


def stop_gamemode(username: str, map_id: str) -> str:
    if not username:
        return json.dumps({"status": "error", "message": "Username is required"})

    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        stop_command = {
            "command": "stop",
            "params": []
        }
        wsock.send(json.dumps(stop_command))
        response = message_queue.get()

        return ensure_json_response(response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })

def send_save_to_server(username: str, map_id: str, command: str) -> str:
    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        save_command = {
            "command": command.lower().replace(" ", "_"),
            "params": []
        }
        wsock.send(json.dumps(save_command))
        save_response = message_queue.get()

        return ensure_json_response(save_response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })
        
def get_comp_id_to_server(username: str, map_id: str, command: str, x:int, y:int) -> str:
    
    try:
        wsock, message_queue, stop_event = maintain_connection(username, map_id)

        save_command = {
            "command": "get_info",
            "params": [map_id, x, y]
        }
        
        wsock.send(json.dumps(save_command))
        save_response = message_queue.get()

        return ensure_json_response(save_response)

    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": f"Error: {str(e)}"
        })        