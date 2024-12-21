import socket

def send_to_server(username: str, command: str, *args):

    host = "127.0.0.1"
    port = 1423

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        client_socket.connect((host, port))

        username_message = f'{username}\n'
        client_socket.sendall(username_message.encode('utf-8'))

        command_string = f'{command}'
        if args:
            command_string += ' ' + ' '.join(map(str, args))

        command_string += '\n'

        client_socket.sendall(command_string.encode('utf-8'))

        response = client_socket.recv(1024).decode('utf-8').strip()

        return response

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        client_socket.close()
