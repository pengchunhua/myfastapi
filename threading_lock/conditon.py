"""
Condition
Condition可以进行多次通知，并通知不同数量的线程，基本的方法如下：

acquire()	#线程锁
release()	#释放锁
wait(timeout)	#线程挂起，直到收到notify
notify(n=1)		#通知至少一个线程
notify_all()	#通知所有线程
前面的两个锁相关方法在此不再赘述，也就是在运行时锁住线程使代码能够完整执行。这里主要说一下wait()和notify()。
"""

import threading
import time

product = [0]
def consumer(cond):
    with cond:
        print('wait for product')
        cond.wait()
        print('get product:{}'.format(product))

def producer(cond):
    product.append(10)
    with cond: 
        cond.notify()	# 唤起一个
        print('notify !')
    time.sleep(3)
    product.append(20)
    with cond:
        cond.notify()	# 再唤起一个
        print('notify !')
    time.sleep(3)
    product.append(30)
    with cond:
        cond.notify_all()	# 全部唤起
        print('notify all!')

condition = threading.Condition()

c1 = threading.Thread(name='c1',target=consumer,args=(condition,))
c2 = threading.Thread(name='c2',target=consumer,args=(condition,))
c3 = threading.Thread(name='c3',target=consumer,args=(condition,))
c4 = threading.Thread(name='c4',target=consumer,args=(condition,))
p = threading.Thread(name='p',target=producer,args=(condition,))

c1.start()
c2.start()
c3.start()
c4.start()

p.start()
