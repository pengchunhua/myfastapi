#!/usr/bin/env python
# encoding: utf-8
import
select
import
signal
import
fcntl
import os
pipe_r， pipe_w = os.pipe()
"rb"，0) # means unbuffered,1是默认buffer数字,具体的数字就是相应数量byte的buffer
#r fd_obi = os.fdopen(r.
#r fd 二
i fd obi.fileno()
flags =
fcntl.fcntl(pipe_w, fcntl.F_GETFL， )
flags = fagsos.O_NONBLOCK
flags
= fcntl.fcntl(pipe_w, fcntl.F_SETFL， flags)
signal.set_wakeup_fd(pipe_w)
# Mask out signal handler
#不设置这个的话,就会运行SIGALRM默认的handler,会打印 alarm clock,然后退出
signal.signal(signal.SIGALRM， lambda x,y: None) #signal.signal(signalnum， handler)
+ Set up a signal to repeat every 2 seconds
#signal.ITIMER_REAL :Decrements interval timer in real time, and delivers SIGALRM upon expiration.
#signal.setitimer(which, seconds[, interval]),The interval timer specified by which can be cleared by seting seconds to zero
signal,setitimer(signal.ITINER_REAL，2，0) # 这个地方的信号量可以由其他线程发送，从而唤醒select及poll中的阻塞等待
poller = select.epoll()
poller.register(pipe_r, select.EPOLLIN)
print "startu
while True:
try:
events = poller.poll()
for fd，flags in events:
"receive Signal
print
print fd，flags
# read a single event
#os.read(fd,n),Read at most n bytes from file descriptor fd.
#Return a string containing the bytes read.
#If the end of the file referred to by fd has been reached, an empty string is returned
print os.read(pipe_r，1)
except IOError:
pass
