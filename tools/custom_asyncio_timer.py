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
    task = asyncio.create_task(print_hello())
    task.add_done_callback(partial(complete, loop))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.call_later(10, kk)
    loop.run_forever()
