import contextlib
import signal
import os
import sys
import socket

print(f"pid is: {os.getpid()}")
class Waker:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #绑定端操作系统会随机分配一个空闲端口
        sock.bind(("127...1", 0))
        host, port = sock.getsockname()
        sock.listen(1)
        self.writer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.writer.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.writer.connect((host, port))
        self.writer.setblocking(False)
        self.reader, _ = sock.accept()
        self.reader.setblocking(False)
        sock.close()

    def consume(self):
        with contextlib.suppress(IOError, socket.error):
            while True :
                data = self.reader.recv(1024)
                if not data:
                    break
                print(repr(data))
                sys.exit(2)

    def get_wakeup_fd(self):
        return self.writer.fileno()

waker = Waker()
def on_sig_int(sn, fo):
    print("on_sig_int")
    waker.consume()

signal.signal(signal.SIGINT, on_sig_int)
signal.set_wakeup_fd(waker.get_wakeup_fd())
while True:
    import time
    time.sleep(0.2)
