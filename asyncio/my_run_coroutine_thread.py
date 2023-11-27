"""
目的：实现asyncio异步的多线程

函数：run_coroutine_threadsafe(coro, loop):

将协程提交给给定的事件循环。线程安全。

返回 concurrent.futures.Future 以等待来自另一个 OS 线程的结果。

此函数意在从与运行事件循环的操作系统线程不同的操作系统线程中调用。例子：
"""

import asyncio, time, threading
 
async def main(i): 
    while True:
        await asyncio.sleep(1)
        print(i)
 
async def production_task():
    for i in "123":
        # 将不同参数main这个协程循环注册到运行在线程中的循环，
        # thread_loop会获得一循环任务
        asyncio.run_coroutine_threadsafe(main(i),thread_loop)
        # 注意：run_coroutine_threadsafe 这个方法只能用在运行在线程中的循环事件使用
 
def start_loop(thread_loop):
     #  运行事件循环， loop以参数的形式传递进来运行
    asyncio.set_event_loop(thread_loop)
    thread_loop.run_forever()
 
if __name__ == '__main__':
    
    # 获取一个事件循环
    thread_loop = asyncio.new_event_loop()
    # 将次事件循环运行在一个线程中，防止阻塞当前主线程，运行线程，同时协程事件循环也会运行
    threading.Thread(target=start_loop,args=(thread_loop,)).start()
    
    # 将生产任务的协程注册到这个循环中
    advocate_loop = asyncio.get_event_loop()
    # 运行次循环
    advocate_loop.run_until_complete(production_task())
