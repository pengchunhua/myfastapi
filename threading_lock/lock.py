import threading
import time

num = 0

lock = threading.RLock()


# 调用acquire([timeout])时，线程将一直阻塞，
# 直到获得锁定或者直到timeout秒后（timeout参数可选）。
# 返回是否获得锁。
def Func():
    lock.acquire()
    global num
    num += 1
    time.sleep(1)
    print(num)
    lock.release()


for i in range(10):
    t = threading.Thread(target=Func)
    t.start()

# 存在的问题：对于Lock对象而言，如果一个线程连续两次release，使得线程死锁。所以Lock不常用，一般采用Rlock进行线程锁的设定。


