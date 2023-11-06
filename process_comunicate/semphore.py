import multiprocessing
import time

def worker(s, i):
    s.acquire()
    print(time.strftime('%Y-%m-%d %H:%M:%S'), multiprocessing.current_process().name + " 抢占并获得锁，运行")
    time.sleep(i)
    print(time.strftime('%Y-%m-%d %H:%M:%S'), multiprocessing.current_process().name + " 运行结束，释放锁")
    s.release()

if __name__ == '__main__':
    s = multiprocessing.Semaphore(2)
    for i in range(8):
        p = multiprocessing.Process(target=worker, args=(s, 1))
        p.start()
