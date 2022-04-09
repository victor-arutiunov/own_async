import socket
from select import select


to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("localhost", 8001))
server_socket.listen()


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    to_monitor.append(client_socket)


def accept_message(client_socket):
    request = client_socket.recv(4096)

    if request:
        message = "Welcome to the club Buddy\n"
        client_socket.send(message.encode())
    else:
        client_socket.close()


def event_loop():
    while True:

        rlist, wlist, xlist = select(to_monitor, [], [])

        for sock in rlist:
            if sock is server_socket:
                accept_connection(sock)
            else:
                accept_message(sock)


if __name__ == "__main__":
    to_monitor.append(server_socket)
    event_loop()
