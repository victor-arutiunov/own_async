import socket
import select


con_num = 0
poll_obj = select.poll()
listen = []
tasks = []


def create_server():
    print("Creating server...")
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind(("localhost", 8001))
    ss.listen()
    return ss


def create_client(ss):
    print("Creating client...")
    cs, addr = ss.accept()
    return cs


def recieve_message(cs):
    print("Recieving message...")
    request = cs.recv(4096)
    return request


def net_road():
    ss = create_server()
    cs = create_client(ss)
    request = recieve_message(cs)
    print(request)


def event_loop():
    pass


create_client()
event_loop()
