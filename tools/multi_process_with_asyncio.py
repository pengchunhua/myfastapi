
import asyncio
import multiprocessing
import os
import time
from multiprocessing import Manager


# 业务类
class BaiJiaHao():

    async def get_author(self, rec):
        """
        协程代码
        """
        print('enter get author,wait for: %d' % rec['num'])
        # 模拟IO操作，耗时根据传进来的num决定
        await asyncio.sleep(rec['num'])
        # 返回协程任务完成后的结果
        return rec


    def run(self):
        # 假定我们有11个任务要跑，每个任务耗时为num秒，串行的话需要43秒。
        # 但我们这个demo跑完只需要这些任务中的最大值：8秒
        list = [{'title': 'title1', 'num': 2},
                {'title': 'title2', 'num': 1},
                {'title': 'title3', 'num': 3},
                {'title': 'title4', 'num': 8},
                {'title': 'title5', 'num': 2},
                {'title': 'title6', 'num': 5},
                {'title': 'title7', 'num': 7},
                {'title': 'title8', 'num': 3},
                {'title': 'title9', 'num': 4},
                {'title': 'title10', 'num': 3},
                {'title': 'title11', 'num': 5},
                ]
        result = run_get_author_in_multi_process(list)
        print('result', result)


def get_chunks(iterable, chunks=1):
    """
    此函数用于分割若干任务到不同的进程里去
    """
    lst = list(iterable)
    return [lst[i::chunks] for i in range(chunks)]


def run_get_author(lists, queue):
    """
    这个就是子进程运行的函数，接收任务列表和用于进程间通讯的Queue
    """
    print('exec run_get_author.child process id : %s, parent process id : %s' % (os.getpid(), os.getppid()))
    # 每个子进程分配一个新的loop
    loop = asyncio.new_event_loop()
    # 初始化业务类，转成task或future
    spider = BaiJiaHao()
    tasks = [loop.create_task(spider.get_author(rec)) for rec in lists]
    # 协程走起
    loop.run_until_complete(asyncio.wait(tasks))
    # 往queue写入每个任务的结果
    for task in tasks:
        queue.put(task.result())


def run_get_author_in_multi_process(task_lists):
    """
    父进程函数，主要是分割任务并初始化进程池，启动进程并返回结果
    """
    # process_count = len(tasks) % 2
    # 进程数这里我用机器上的核心数，注意：未考虑核心数比任务多的情况
    process_count = multiprocessing.cpu_count()
    print('process_count: %d' % process_count)
    split_lists = get_chunks(task_lists, process_count)
    pool = multiprocessing.Pool(process_count)
    queue = Manager().Queue()
    for lists in split_lists:
        pool.apply_async(run_get_author, args=(lists, queue,))
    pool.close()
    pool.join()
    result = []
    # 从子进程读取结果并返回
    while not queue.empty():
        result.append(queue.get())
    return result

now = lambda : time.time()

if __name__ == '__main__':
    start = now()
    spider = BaiJiaHao()
    spider.run()
    print('done','TIME: ', now() - start)
