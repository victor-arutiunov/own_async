import socket
from async_socket import Async


def create_server():
    print("Creating server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8001))
    server_socket.listen()
    while True:
        yield server_socket
        Async.add_task(create_client(server_socket))


def create_client(server_socket):
    print("Creating client...")
    client_socket, addr = server_socket.accept()
    while True:
        yield client_socket
        message = recieve_message(client_socket)
        if not message:
            break


def recieve_message(client_socket):
    print("Recieving message...")
    request = client_socket.recv(4096)
    if not request:
        return False
    else:
        return True
        print(request)


Async.add_task(create_server())
Async.event_loop()
