"""
1.5 基于有名管道（fifo）的IPC
相对于管道只能用于父子进程之间通信，Unix还提供了有名管道可以让任意进程进行通信。有名管道又称fifo，它会将自己注册到文件系统里一个文件，参数通信的进程通过读写这个文件进行通信。
fifo要求读写双方必须同时打开才可以继续进行读写操作，否则打开操作会堵塞直到对方也打开。
"""

# ---------------------------------------读端--------------------------------------------
#encoding:utf-8
import os, time, random
 
p_Name = "./pipe1"
 
if (os.access(p_Name, os.F_OK) == False) :
    os.mkfifo(p_Name)
 
print "before open"
fp_r = os.open(p_Name, os.O_RDONLY)
print "open end"
while True:
    msg = os.read(fp_r, 100)
    if msg == "":
        break
    print msg
    if msg == "q":
        print "quit"
        break
os.close(fp_r)

# ---------------------------------写端------------------------------------------------
#encoding:utf-8
import os
 
p_Name = "./pipe1"
 
if os.access(p_Name, os.F_OK) == False:
    os.mkfifo(p_Name)
fd_w = os.open(p_Name, os.O_WRONLY)
 
while True:
    msg = raw_input("w---->>")
    os.write(fd_w, msg)
    if msg == "q":
        break
os.close(fd_w)


# 参考程序
import os
import sys
import math


def slice(mink, maxk):
    s = 0.0
    for k in range(mink, maxk):
        s += 1.0/(2*k+1)/(2*k+1)
    return s


def pi(n):
    childs = []
    unit = n / 10
    fifo_path = "/tmp/fifo_pi"
    os.mkfifo(fifo_path)  # 创建named pipe
    for i in range(10):  # 分10个子进程
        mink = unit * i
        maxk = mink + unit
        pid = os.fork()
        if pid > 0:
            childs.append(pid)
        else:
            s = slice(mink, maxk)  # 子进程开始计算
            with open(fifo_path, "w") as ff:
                ff.write(str(s) + "\n")
            sys.exit(0)  # 子进程结束
    sums = []
    while True:
        with open(fifo_path, "r") as ff:
            # 子进程关闭写端，读进程会收到eof
            # 所以必须循环打开，多次读取
            # 读够数量了就可以结束循环了
            sums.extend([float(x) for x in ff.read(1024).strip().split("\n")])
            if len(sums) == len(childs):
                break
    for pid in childs:
        os.waitpid(pid, 0)  # 等待子进程结束
    os.unlink(fifo_path)  # 移除named pipe
    return math.sqrt(sum(sums) * 8)
