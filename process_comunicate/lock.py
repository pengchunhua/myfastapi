from multiprocessing import Process
from multiprocessing import Lock
import time
import random

def task1(p, lock):
    # 上锁
    lock.acquire()
    print(f'{p} 开始排泄')
    time.sleep(random.randint(1, 3))
    print(f'{p} 排泄结束')
    # 解锁
    lock.release()

def task2(p, lock):
    lock.acquire()
    print(f'{p} 开始排泄')
    time.sleep(random.randint(1, 3))
    print(f'{p} 排泄结束')
    lock.release()

def task3(p, lock):
    lock.acquire()
    print(f'{p} 开始排泄')
    time.sleep(random.randint(1, 3))
    print(f'{p} 排泄结束')
    lock.release()


if __name__ == '__main__':
    # 实例化一个锁对象
    mutex = Lock()
    # 将锁以参数的形式传入进程对象
    p1 = Process(target=task1, args=('task1', mutex,))
    p2 = Process(target=task2, args=('task2', mutex,))
    p3 = Process(target=task3, args=('task3', mutex,))

    p1.start()
    p2.start()
    p3.start()
