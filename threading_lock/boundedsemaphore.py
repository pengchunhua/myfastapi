"""
一、Semaphore对象
1. 基本介绍

Semaphore 是最古老的同步原语之一，由荷兰计算机科学家 Edsger W. Dijkstra 发明。（他最早使用名为 P() 和 V() 的函数对应 acquire() 和 release()）
Semaphore 在内部管理着一个计数器。调用 acquire() 会使这个计数器 -1，release() 则是+1.计数器的值永远不会小于 0，当计数器到 0 时，再调用 acquire() 就会阻塞，直到其他线程来调用release()
Semaphore 也支持上下文管理协议
class threading.Semaphore(value=1)

acquire(blocking=True,timeout=None)

本方法用于获取 Semaphore
当使用默认参数调用本方法时：如果内部计数器的值大于零，将之减一，并返回；如果等于零，则阻塞，并等待其他线程调用 release() 方法以使计数器为正。
这个过程有严格的互锁机制控制，以保证如果有多条线程正在等待解锁，release() 调用只会唤醒其中一条线程。唤醒哪一条是随机的。本方法返回 True，或无限阻塞
如果 blocking=False，则不阻塞，但若获取失败的话，返回 False
当设定了 timeout 参数时，最多阻塞 timeout 秒，如果超时，返回 False
release()

释放 Semaphore，给内部计数器 +1，可以唤醒处于等待状态的线程
"""
# coding: utf-8
import threading
import time


def fun(semaphore, num):
    # 获得信号量，信号量减一
    semaphore.acquire()
    print "Thread %d is running." % num
    time.sleep(3)
    # 释放信号量，信号量加一
    semaphore.release()


if __name__=='__main__':
    # 初始化信号量，数量为2
    semaphore = threading.Semaphore(2)

    # 运行4个线程
    for num in xrange(4):
        t = threading.Thread(target=fun, args=(semaphore, num))
        t.start()

"""
二、BoundedSemaphore对象
1. 基本介绍

一个工厂函数，返回一个新的有界信号量对象。一个有界信号量会确保它当前的值不超过它的初始值。如果超过，则引发ValueError。在大部分情况下，信号量用于守护有限容量的资源。
如果信号量被释放太多次，它是一种有bug的迹象。如果没有给出，value默认为1。

class threading.BoundedSemaphore(value=1)

本类用于实现 BoundedSemaphore 对象。BoundedSemaphore 会检查内部计数器的值，并保证它不会大于初始值，如果超了，就引发一个 ValueError。
多数情况下，semaphore 用于守护限制访问（但不限于 1）的资源，如果 semaphore 被 release() 过多次，这意味着存在 bug
"""
# coding: utf-8
import threading
import time


def fun(semaphore, num):
    # 获得信号量，信号量减一
    semaphore.acquire()
    print "Thread %d is running." % num
    time.sleep(3)
    # 释放信号量，信号量加一
    semaphore.release()
    # 再次释放信号量，信号量加一，这是超过限定的信号量数目，这时会报错ValueError: Semaphore released too many times
    semaphore.release()


if __name__=='__main__':
    # 初始化信号量，数量为2，最多有2个线程获得信号量，信号量不能通过释放而大于2
    semaphore = threading.BoundedSemaphore(2)

    # 运行4个线程
    for num in xrange(4):
        t = threading.Thread(target=fun, args=(semaphore, num))
        t.start()
