import time
def time_it(func):
  def __inner(*args, **kwargs):
    start = time.time()
    res = func(*args, **kwargs)
    print(f"spend time:{time.time()-start}")
    return res
  return __inner

@time_it
def run():
  print("start running")
  time.sleep(3)

if __name__ == "__main__":
  run()
  
