# 长连接服务端程序
import socket 
from struct import unpack

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("", 6666))
sock.listen(5)

conn, addr = sock.accept()
conn.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
conn.ioctl(socket.SIO_KEEPALIVE_VALS, 
    (1,  # 开启保活机制
    60*1000,  # 1分钟后如果对方还没有反应，开始探测链接是否存在
    30 * 1000  # 60秒钟探测一次，默认10次，失败则断开
))
while True:
    data_length = conn.recv(4)
    if not data_length:
        break
    data_length = unpack("i", data_length)[0]
    data = conn.recv(data_length).decode()
    print(data)


# 长连接客户端
import socket
from time import sleep
from struct import pack
from datetime import datetime

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, True)
sock.ioctl(socket.SIO_KEEPALIVE_VALS, 
    (1,  # 开启保活机制
    60*1000,  # 1分钟后如果对方还没有反应，开始探测链接是否存在
    30 * 1000  # 60秒钟探测一次，默认10次，失败则断开
))
sock.connect(("localhost", 6666))
for _ in range(5):
    msg = str(datetime.now())[:19]
    print(msg)
    msg = msg.encode()
    sock.sendall(pack("i", len(msg)))
    sock.sendall(msg)
    sleep(600)
sock.close()
