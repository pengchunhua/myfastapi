# 说明：loop的call_later/call_soon/call_at等函数只能调用非协程函数，所以需要将任务封装成task后调用

import asyncio
from functools import partial

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
