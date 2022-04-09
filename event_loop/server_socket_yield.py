import socket
from select import select


tasks = []

sockets_to_read = {}
sockets_to_write = {}
# sockets = {}


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
            # yield ("write", client_socket)
            client_socket.send(response)

    client_socket.close()


def listener(tasks):
    # listen while tasks become available and append them to tasks list

    while not tasks:
        ready_to_read, ready_to_write, _ = select(sockets_to_read, sockets_to_write, [])

        for sock in ready_to_read:
            tasks.append(sockets_to_read.pop(sock))

        for sock in ready_to_write:
            tasks.append(sockets_to_write.pop(sock))


def event_loop():
    # executes tasks and append sockets to socket listener

    while any([tasks, sockets_to_read, sockets_to_write]):
        listener(tasks)

        try:
            task = tasks.pop(0)
            reason, sock = next(task)

            if reason == "read":
                sockets_to_read[sock] = task
            if reason == "write":
                sockets_to_write[sock] = task

        except StopIteration:
            print("Done")


if __name__ == "__main__":
    server = create_server()
    tasks.append(server)
    event_loop()
