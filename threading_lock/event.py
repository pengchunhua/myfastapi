"""
使用Event来对线程进行阻塞操作，Event对象有四个基本的方法，创建实例时flag被设置为false。

wait()	# 阻塞，直到flag被设置为true或者超时
set()		# 执行，将event内部的flag设置为true
clear()	# 清除标识位，重新设置为false
isSet()	# 判断flag是否为true
"""

import time
from threading import Thread,Event

def countdown(n,started_evt):
	print('countdown starting')
	while n > 0:
		print('T-minus',n)
		if n == 7:
			started_evt.set()	# 第一次停止阻塞
		if n < 3 and started_evt.isSet() == False:
			started_evt.set()	# 第二次停止阻塞
		n -= 1
		time.sleep(2)

started_evt = Event()
t = Thread(target=countdown,args=(10,started_evt))
t.start()

started_evt.wait()	# 第一次阻塞
for i in range(20):
	print('main count :{}'.format(i))
	if i == 10:
		started_evt.clear()
		started_evt.wait()	# 再次阻塞
