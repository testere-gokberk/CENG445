import socket

def send_to_server(username: str, command: str, *args):

    host = "127.0.0.1"
    port = 1423

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        server_prompt = client_socket.recv(1024).decode('utf-8').strip()

        username_message = f'{username}\n'
        client_socket.sendall(username_message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8').strip()


        command_string = f'{command}'
        if args:
            command_string += ' ' + ' '.join(map(str, args))
        command_string += '\n'
        client_socket.sendall(command_string.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8').strip()
        print(response)
        return response

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        client_socket.close()
def send_component_to_server(username: str, map_id, component: str, row, col):

    host = "127.0.0.1"
    port = 1423
    print("retret")
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        server_prompt = client_socket.recv(1024).decode('utf-8').strip()

        username_message = f'{username}\n'
        client_socket.sendall(username_message.encode('utf-8'))
        username_response = client_socket.recv(1024).decode('utf-8').strip()
        print("111")

        attach_string = f'attach {map_id}\n'
        client_socket.sendall(attach_string.encode('utf-8'))
        attach_response = client_socket.recv(1024).decode('utf-8').strip()

        print("222")

        create_string = f'create {component}\n'

        client_socket.sendall(create_string.encode('utf-8'))
        create_response = client_socket.recv(1024).decode('utf-8').strip()

        component_id  = client_socket.recv(1024).decode('utf-8').strip()
        print("333")
        place_string = f'place {component_id} {row} {col}\n'

        client_socket.sendall(place_string.encode('utf-8'))
        print("444")
        place_response = client_socket.recv(1024).decode('utf-8').strip()

        detach_string = f'detach {map_id}\n'
        client_socket.sendall(detach_string.encode('utf-8'))
        detach_response = client_socket.recv(1024).decode('utf-8').strip()


        print(attach_response,create_response,place_response,detach_response)


        return f'{place_response}\n'

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        client_socket.close()


def send_delete_to_server(username: str,map_id, command: str, *args):

    host = "127.0.0.1"
    port = 1423

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        server_prompt = client_socket.recv(1024).decode('utf-8').strip()

        username_message = f'{username}\n'
        client_socket.sendall(username_message.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8').strip()

        attach_string = f'attach {map_id}\n'
        client_socket.sendall(attach_string.encode('utf-8'))
        attach_response = client_socket.recv(1024).decode('utf-8').strip()


        command_string = f'{command}'
        if args:
            command_string += ' ' + ' '.join(map(str, args))
        command_string += '\n'
        client_socket.sendall(command_string.encode('utf-8'))

        command_response = client_socket.recv(1024).decode('utf-8').strip()

        detach_string = f'detach {map_id}\n'
        client_socket.sendall(detach_string.encode('utf-8'))
        detach_response = client_socket.recv(1024).decode('utf-8').strip()

        print(attach_response,command_response,detach_response)
        return f'{command_response}\n'

    except Exception as e:
        print(f"Error: {e}")
        return None

    finally:
        client_socket.close()