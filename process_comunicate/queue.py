# 操作系统提供了跨进程的消息队列对象可以让我们直接使用，但是python没有默认提供包装好的api来直接使用。我们必须使用第三方扩展来完成OS消息队列通信。第三方扩展是通过使用Python包装的C实现来完成的。


#! usr/bin/python3.6
# -*- coding:utf-8 -*-
from multiprocessing import Process, Queue
import random, time, os
# 写数据进程执行的代码
def proc_write(q, urls):
    print("Process %s is writing..." %os.getpid())
    for url in urls:
        q.put(url)
        print("Put %s to queue..." %url)
        time.sleep(random.random())
 
# 读数据进程执行的代码
def proc_read(q):
    print("Process %s is reading...." % os.getpid())
    while True:
        url = q.get(True)
        print("Get %s from queue." %url)
 
if __name__ == '__main__':
    # 父进程创建Queue,并传给各个子进程
    q = Queue()
    proc_write1 = Process(target= proc_write, args=(q, ['url_1', 'url_2', 'url_3']))
    proc_write2 = Process(target= proc_write, args=(q, ['url_4', 'url_5', 'url_6']))
    proc_reader = Process(target= proc_read, args=(q,))
    # 启动子进程proc_write, 写入
    proc_write1.start()
    proc_write2.start()
    #启动子进程proc_read，读取
    proc_reader.start()
    # 等待proc_writer结束
    proc_write1.join()
    proc_write2.join()
    # proc_reader进程里是死循环，无法等待其结束，只能强行终止
    proc_reader.terminate()
