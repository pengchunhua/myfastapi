import queue
import socket
import os
import select
import threading
import time

class PollableQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        # Create a pair of connected sockets
        if os.name == 'posix':
            # 创建系统内部的socket，主要是为了使用网卡的写和读事件来通知的，在linux中的事件循环也是采用了这种机制
            self._putsocket, self._getsocket = socket.socketpair()
        else:
            # Compatibility on non-POSIX systems
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('127.0.0.1', 0))
            server.listen(1)
            self._putsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._putsocket.connect(server.getsockname())
            self._getsocket, _ = server.accept()
            server.close()

    def fileno(self):
        return self._getsocket.fileno()

    def put(self, item):
        super().put(item)
        self._putsocket.send(b'x')

    def get(self):
        self._getsocket.recv(1)
        return super().get()


def consumer(queues):
    '''
    Consumer that reads data on multiple queues simultaneously
    '''
    while True:
        # 阻塞获取事件通知，一旦有事件通知则继续往后执行， 这里其实可以用os.pipe()或者一个埋点的socketpair来实现手动唤醒select,从而执行下面的行为
        can_read, _, _ = select.select(queues,[],[])
        for r in can_read:
            item = r.get()
            print('Got:', item)

q1 = PollableQueue()
q2 = PollableQueue()
q3 = PollableQueue()
t = threading.Thread(target=consumer, args=([q1,q2,q3],))
t.daemon = True
t.start()

# Feed data to the queues
q1.put(1)
q2.put(10)
q3.put('hello')
q2.put(15)
# 注意：这里只是为了主线程不要快速退出
time.sleep(10)
