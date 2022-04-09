import socket
from async_socket import AsyncSocket


def create_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 8001))
    server_socket.listen()

    while True:
        yield ("read", server_socket)
        client_socket, addr = server_socket.accept()
        print("Connections from: ", addr)
        client = create_client(client_socket)
        tasks.append(client)


def create_client(client_socket):
    while True:
        yield ("read", client_socket)
        request = client_socket.recv(4096)
        if not request:
            break
        else:
            response = "Hello wolrd\n".encode()
            yield ("write", client_socket)
            client_socket.send(response)

    client_socket.close()


server = create_server()
tasks.append(server)
event_loop()
