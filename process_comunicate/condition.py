from multiprocessing import Process, Condition
import time

cond = Condition()

class MyProcess1(Process):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        cond.acquire()

        print('%s说：1' % self.name)
        cond.notify()
        cond.wait()

        # 等待2秒
        time.sleep(2)
        print('%s说：11' % self.name)
        cond.notify()
        cond.wait()

        time.sleep(2)
        print('%s说：111' % self.name)
        cond.notify()

        cond.release()

class MyProcess2(Process):
    def __init__(self, name):
        super().__init__(name=name)

    def run(self):
        time.sleep(1)
        cond.acquire()

        # 等待2秒
        time.sleep(2)
        print('%s说：2' % self.name)
        cond.notify()
        cond.wait()

        time.sleep(2)
        print('%s说：22' % self.name)
        cond.notify()
        cond.wait()

        time.sleep(2)
        print('%s说：222' % self.name)

        cond.release()

MyProcess1('Process1').start()
MyProcess2('Process2').start()
