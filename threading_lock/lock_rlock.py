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

import threading
mylock = threading.RLock()
num = 0
class WorkThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.t_name = name
      
    def run(self):
        global num
        while True:
            mylock.acquire()
            print('\n%s locked, number: %d' % (self.t_name, num))
            if num >= 2:
                mylock.release()
                print('\n%s released, number: %d' % (self.t_name, num))
                break
            num += 1
            print('\n%s released, number: %d' % (self.t_name, num))
            mylock.release()
def test():
    thread1 = WorkThread('A-Worker')
    thread2 = WorkThread('B-Worker')
    thread1.start()
    thread2.start()
if __name__ == '__main__':
    test() 

# 注意lock.acquire()与lock.release()有时候容易忘记成对出现从而死锁，所以最好的方式是使用with语句来实现。
