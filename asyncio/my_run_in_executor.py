# ===============================run_in_executor=================================
# asyncio.run_in_executor函数主要是异步调用同步方法

from concurrent.futures import ThreadPoolExecutor
import asyncio,time

def test(): #测试的阻塞函数
   time.sleep(10)
   threadmingzi()
   return "after 10s"
           
async def returnfuture(): #测试新建线程
  loop=asyncio.get_event_loop() 
  executor=ThreadPoolExecutor()
  future=await loop.run_in_executor(executor,test)#执行阻塞函数
  print(future)
        
asyncio.run(returnfuture())
