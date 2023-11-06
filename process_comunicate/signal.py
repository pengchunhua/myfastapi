"""
Python标准库signal模块提供了在 Python 程序中使用信号处理程序的机制。信号处理程序总是在 Python 主线程中执行，即使信号是在另一个线程中接收的。所以信号不能用作线程间通信的手段，如果需要线程间通信可以使用 threading 模块中的同步函数。此外，只允许主线程设置新的信号处理程序。

信号通信的应用：
（1）故障定位技术(进程的底层故障，例如进程突然中断和一些可能性较小的故障)；
（2）对进程的流程控制 ；

signal常用的几个函数
（1）os.kill(pid,sig)
用于从一个进程中发送一个信号给某个进程。
参数解析：
pid 指定发送信号的进程号
sig 要发送的信号代号(需要通过signal模块获取)
(2)signal.alarm(sec)
设置时钟信号，在一定时间后给自身发送一个SIGALRM信号。非阻塞函数，sec为定时长度。
原理:
时钟的创建是进程交由操作系统内核(kernal)帮助创建的，时钟和进程之间是异步执行的,当时钟到时,内核会发送信号给进程,进程接收信号进行相应的响应操作。这就是所谓的python异步处理方案。后面的时钟会覆盖前面的时钟,一个进程。只有一个挂起的时钟
"""

import signal, os

def handler(signum, frame):
    '''
    信号处理程序
    '''
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")

# 设置信号处理器
signal.signal(signal.SIGALRM, handler)
# 设置5s的定时,时间到后给自身发送一个SIGALRM信号
signal.alarm(5)

# open()可能无限等待，或者打开资源的时间过长
fd = os.open('/dev/ttyS0', os.O_RDWR)
# 关闭定时
signal.alarm(0)
