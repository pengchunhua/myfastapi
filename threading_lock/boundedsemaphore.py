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
