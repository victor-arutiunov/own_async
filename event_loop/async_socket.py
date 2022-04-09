from select import select


class AsyncSocket():
    last_task_number = 0
    tasks = []
    listen = {}
    poll_obj = select.poll()

    @classmethod
    def listener(cls, tasks):
        # listen while tasks become available and append them to tasks list

        while not tasks:
            for lis in cls.listen:
                cls.poll_obj.register(lis[0], select.POLLIN)
                cls.poll_obj.register(lis[0], select.POLLOUT)
            rtr, rtw, _ = select(cls.listen, cls.listen, [])

            for sock in rtr + rtw:
                tasks.append(cls.listen.pop(sock))

    @classmethod
    def event_loop(cls):
        # executes tasks and append sockets to socket listener

        while any([cls.tasks, cls.listen]):
            cls.listener(cls.tasks)

            try:
                task = cls.tasks.pop(0)
                reason, sock = next(task)
                cls.listen.append((reason, sock))

            except StopIteration:
                print("Done")
