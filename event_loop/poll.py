import socket
import select


def create_server():
    print("Creating server...")
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(("localhost", 8001))
    ss.listen()
    return ss


poll_obj = select.poll()
ss = create_server()


poll_obj.register(ss, select.POLLIN)
poll_obj.register(ss, select.POLLHUP)
print(poll_obj.poll())
