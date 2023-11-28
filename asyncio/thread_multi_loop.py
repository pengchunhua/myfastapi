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
            await asyncio.wait_for(fut, 3)
        except asyncio.TimeoutError:
            continue
        if fut.done():
            break
    print(f"spend time:{loop.time()-start}")


async def main(loop):
    start = loop.time()
    print(f"main, time:{start}, loop:{id(asyncio.get_event_loop())}, pid:{os.getpid()}")
    Thread(target=asyncio.run_coroutine_threadsafe, args=(adjust(), asyncio.get_event_loop())).start()
    await asyncio.sleep(10)
    if not waiter_dict["waiter"].done():
        waiter_dict["waiter"].set_result(None)
    await asyncio.sleep(1)

async def test(loop):
    start = loop.time()
    time.sleep(3)  # 因为这里是同步阻塞的，如果使用相同的事件循环会相互阻塞，导致不同的协程之间相互干扰
    print(f"test, time:{start}, loop:{id(loop)}, pid:{os.getpid()}")
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
  loop = asyncio.get_event_loop()
  thread_loop = asyncio.new_event_loop()
  Thread(target=thread_main, args=(thread_loop, )).start()
  # # Thread(target=asyncio.run_coroutine_threadsafe, args=(test(thread_loop), thread_loop)).start()
  loop.run_until_complete(main(loop))
  
