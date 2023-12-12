import asyncio
from functools import wraps, partial

import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()


def timer(func=None, interval=60):
    if func is None:
        return partial(timer, interval=interval)

    @wraps(func)
    async def decorated(*args, **kwargs):
        while True:
            await asyncio.sleep(interval, loop=loop)
            await func(*args, **kwargs)
    return loop.create_task(decorated())


@timer(interval=1)
async def func1():
    print(1)


@timer(interval=5)
async def func2():
    print(2)


loop.run_forever()
