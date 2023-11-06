"""
# 障碍对象barrier 
barrier = threading.Barrier(parties, action=None, timeout=None)
barrier.wait(timeout=timeout)
"""

#Barrier 栅栏
import threading,logging
logging.basicConfig(level=logging.INFO,format="[-] %(threadName)s %(message)s")
 
def work(barrier:threading.Barrier):
    logging.info("n_waiting = {}".format(barrier.n_waiting))   # 等待的线程数
    bid = barrier.wait()   # 参与者的id，返回0到线程数减1的数值
    logging.info("after barrier {}".format(bid))  # 栅栏之后
 
barrier = threading.Barrier(3) # 3个参与者，每3个开闸放行，0,1,2  4,5,6


"""
Barrier实例的方法：

broken  检测栅栏是否处于打破的状态，返回True或False

abort()  将栅栏置于broken状态，等待中的线程或者调用等待方法的线程都会抛出threading.BrokenBarrieError异常，直到reset方法来恢复栅栏

reset()  恢复栅栏，重新开始拦截
"""

#Barrier 栅栏
import threading,logging
logging.basicConfig(level=logging.INFO,format="[-] %(threadName)s %(message)s")
 
def work(barrier:threading.Barrier):
    logging.info("n_waiting = {}".format(barrier.n_waiting))
    try:
        bid = barrier.wait()
        logging.info("after barrier {}".format(bid))
    except threading.BrokenBarrierError:
        logging.info("Broken Barrier in {}".format(threading.current_thread()))
 
barrier = threading.Barrier(3)
 
for x in range(1,12): #12个
    if x == 3:
        barrier.abort() #有一个人坏了规矩
    elif x == 6:
        barrier.reset()
    threading.Event().wait(1)
    threading.Thread(target=work,args=(barrier,),name="Barrier-{}".format(x)).start()

"""
wait方法在等待超时1秒后，就强制将栅栏置于broken状态，直到第6个的时候才reset恢复，然后6,7,8放行，9,10,继续阻塞。如果此时有第11个，就会9,10,11放行。
"""
#Barrier 栅栏
import threading,logging
logging.basicConfig(level=logging.INFO,format="[-] %(threadName)s %(message)s")
 
def work(barrier:threading.Barrier,i:int):
    logging.info("n_waiting = {}".format(barrier.n_waiting))
    try:
        if i < 3:
            bid = barrier.wait(1)  #超时1秒就将栅栏置于broken状态，抛出异常后续语句不会执行
        else:
            if i == 6:
                barrier.reset() #恢复栅栏
            bid = barrier.wait()
        # logging.info("broken status = {}".format(barrier.broken))  #是否处于broken状态
        logging.info("after barrier {}".format(bid))
    except threading.BrokenBarrierError:
        logging.info("Broken Barrier in {}".format(threading.current_thread()))
 
barrier = threading.Barrier(3)
 
for i in range(1,11): #10个
    threading.Event().wait(2) #强制延迟2秒,让出时间片
    threading.Thread(target=work,args=(barrier,i),name="Barrier-{}".format(i)).start()

