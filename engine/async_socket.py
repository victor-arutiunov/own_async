import select
from pprint import pprint
from typing import List, Dict


class Async():
    con_num: int = 1
    poll_ojb = select.epoll()
    poll_events = select.EPOLLIN | select.EPOLLERR | select.EPOLLHUP | select.EPOLLRDHUP

    tasks: List = []
    listen: Dict = {}
    register: Dict = {}

    @classmethod
    def event_loop(cls):
        while True:

            while any(cls.tasks):  # excecuting tasks
                task = cls.tasks.pop(0)
                try:
                    socket = next(task)
                except Exception:
                    continue
                cls.listen[cls.con_num] = {"socket": socket, "task": task}
                cls.register[cls.con_num] = {"socket": socket, "task": task}
                cls.con_num += 1

            if any(cls.register):  # add sockets to register
                for listen_key in cls.register:
                    future = cls.register[listen_key]
                    cls.poll_ojb.register(future["socket"], cls.poll_events)
                cls.register = {}

            ready_sockets: List = cls.poll_ojb.poll()  # get ready sockets
            pprint(ready_sockets)

            for socket in ready_sockets:  # add yields from ready sockets to tasks
                ready_listen_keys: Dict = {key: cls.listen[key] for key in cls.listen if cls.listen[key]["socket"].fileno() == socket[0]}
                cls.poll_ojb.unregister(socket[0])
                for key in ready_listen_keys:
                    del cls.listen[key]
                    if socket[1] != 8193:
                        cls.tasks.append(ready_listen_keys[key]["task"])

    @classmethod
    def add_task(cls, task):
        cls.tasks.append(task)
