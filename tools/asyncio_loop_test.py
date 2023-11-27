# 字符串反转
import asyncio
from asyncio import Event
from functools import partial
from threading import Event, Thread

asyncio.futures.Future
asyncio.wait

async def print_hello():
    print("hello world")
    await asyncio.sleep(3)
    print("complete")
    return 10

def complete(loop, future):
    print(f"result: {future.result()}")
    loop.stop()

def kk():
    task = asyncio.create_task(print_hello())  # 将协程封装为task任务
    task.add_done_callback(partial(complete, loop))  # 任务完成后的回调函数，注意该函数的参数必须带future,如果需要其他参数可以使用partial来设置默认值

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(10, kk)  # 将对应的task任务封装成Handle、TimerHandle，之后调度器使用hanle中的run方法调用执行对应的任务
    loop.run_forever()


# ==============================使用协程完成电压抬升逻辑框架====================================
import time
waiter_dict = {"waiter": None}

async def adjust():
    loop = asyncio.get_running_loop()
    start = loop.time()
    while True:
        print("adjust")
        # await asyncio.sleep(3)
        fut = loop.create_future()
        waiter_dict["waiter"] = fut
        try:
            await asyncio.wait_for(fut, 3)  # 这里是为了防止最后一个判断情况下仍然需要调整的问题，只要future被设值就会中断等待，直接结束电压抬升流程
        except asyncio.TimeoutError:
            continue
        if fut.done():
            break
    print(f"spend time:{loop.time()-start}")

async def main():
    start = loop.time()
    print(f"main, time:{start}, loop:{id(asyncio.get_event_loop())}")
    Thread(target=asyncio.run_coroutine_threadsafe, args=(adjust(), asyncio.get_event_loop())).start()
    await asyncio.sleep(10)
    if not waiter_dict["waiter"].done():
        waiter_dict["waiter"].set_result(None)
    await asyncio.sleep(10)

if __name__ == "__main__":
      asyncio.run(main())

# =========================不同事件循环调度使用的两种实现方式===============================================
async def test(loop):
    time.sleep(3)  # 因为这里是同步阻塞的，如果使用相同的事件循环会相互阻塞，导致不同的协程之间相互干扰，所以最好使用新建线程的方式来实现
    start = loop.time()
    print(f"test, time:{start}, loop:{id(loop)}")
    await asyncio.sleep(5)
    fut = loop.create_future()
    try:
        await asyncio.wait_for(fut, 2)
    except asyncio.TimeoutError:
        print("time out")
    print(f"test complete, spend:{loop.time()-start}")

def thread_main(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(test(loop))

if __name__ == "__main__":
    thread_loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    Thread(target=thread_main, args=(thread_loop,)).start()
    # Thread(target=asyncio.run_coroutine_threadsafe, args=(test(loop), loop)).start()
  # Thread(target=asyncio.run_coroutine_threadsafe, args=(test(thread_loop), thread_loop)).start()
    loop.run_until_complete(main())
