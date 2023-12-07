import asyncio
from aiopools import AsyncPool


async def block_io(i):
    await asyncio.sleep(1)
    print(i)
    return i


async def main():
    # 设置最大允许的协程数 maxio
    async with AsyncPool(maxio=20) as pool:
        tasks = [pool.create_task(block_io(i)) for i in range(100)]
    
    response = await asyncio.gather(*tasks)
    print(response)
    

if __name__ == '__main__':
    asyncio.run(main())


# AsyncPool的源码：
import asyncio


class AsyncPool:
    
    def __init__(self, maxio: int = 20):
        '''
            maxio: The maximum number of coroutines allowed by the system.
        '''
        self.semaphore = asyncio.Semaphore(maxio)
        self.tasks = []
    
    async def create_task(self, task):
        async with self.semaphore:
            return await task

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
