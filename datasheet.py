"""
python实现定时器：https://blog.csdn.net/qq_38412868/article/details/100711702
python描述器：https://zhuanlan.zhihu.com/p/52708890
python元类和元类编程：https://zhuanlan.zhihu.com/p/114242597
property实现原理及实现：https://zhuanlan.zhihu.com/p/142029367
netty能做什么：https://www.zhihu.com/question/24322387
Java NIO wakeup实现原理：https://www.cnblogs.com/yungyu16/p/13065194.html
python实现异步的底层原理是什么：https://www.zhihu.com/question/432814091
python实现简单事件循环：https://zhuanlan.zhihu.com/p/71511434
python调用k8s API:https://www.cnblogs.com/linu/p/11703438.html
python通过k8s API实现集群认证：https://blog.csdn.net/anqixiang/article/details/114434578
python zookeeper实现服务注册与发现：https://blog.csdn.net/weixin_43866211/article/details/103028284
zookeeper实现分布式锁：
  1、https://www.cnblogs.com/zhaobin022/p/8065317.html
  2、https://zhuanlan.zhihu.com/p/363323742
  3、https://www.cnblogs.com/zhaobin022/p/8065317.html
mysql锁机制问题：https://zhuanlan.zhihu.com/p/48269420
python signal.set_wakeup_fd的作用和实现：http://timd.cn/python/signal/
tornado使用signal.set_wakeup_fd的代码：
  1、https://github.com/tao12345666333/tornado-zh/blob/master/tornado/platform/common.py#L10
  2、https://github.com/tao12345666333/tornado-zh/blob/master/tornado/ioloop.py
python signal的使用方式：https://zhuanlan.zhihu.com/p/91678827
python的信号处理库（事件通知库）：
  1、https://zhuanlan.zhihu.com/p/435076618
  2、https://github.com/pallets-eco/blinker/tree/main/src/blinker
linux内核阻塞和异步机制原理：
  1、https://zhuanlan.zhihu.com/p/461439093
  2、https://blog.csdn.net/m0_46535940/article/details/124664708

redis键空间通知：
  1、https://zhuanlan.zhihu.com/p/103963089
  2、https://www.cnblogs.com/fu-yong/p/9628965.html

kafka架构和源码：
  1、从源码到架构全部讲透：https://zhuanlan.zhihu.com/p/388355017
  2、kafka设计架构详解：https://blog.csdn.net/qq_32828253/article/details/110732652
  3、kafka架构及网络设计原理：https://zhuanlan.zhihu.com/p/95502201
  4、kafka数据持久化机制：https://www.jianshu.com/p/1bdc181a7ebd
  5、kafka的ACK机制：https://juejin.cn/post/7166529283291086879
  6、kafka消费者轮询的准备工作：https://blog.csdn.net/baidu_40468340/article/details/128492534

Linux性能调优：
  1、https://zhuanlan.zhihu.com/p/470749806

python监听鼠标和键盘事件：
  1、keybord插件监听键盘事件：https://blog.csdn.net/coco56/article/details/107847467
  2、pynput监听鼠标和键盘事件：https://blog.csdn.net/u011367482/article/details/106173994

事件驱动：
  1、详解事件驱动event实现：https://blog.csdn.net/brucewong0516/article/details/84031715

SSE服务：
  1、python中实现websocket和SSE实现HTTP:https://blog.csdn.net/weixin_44777680/article/details/114692497

threading中Local类的使用：
  1、threading中Local类的使用：https://blog.csdn.net/brucewong0516/article/details/84589806?spm=1001.2014.3001.5502

asyncio事件循环：
  1、多线程中启用多个事件循环：https://www.jianshu.com/p/29ffdbd65679
  2、从0到精通事件循环：https://juejin.cn/post/7240427838343577655

asyncio时间循环的执行过程：
1、通过asyncio创建并初始化loop
2、loop初始化过程：
  一、事件的调度过程：
    1、调用asyncio/base_events.py中的BaseEvent，使用run_until_complete() -> run_forever() -> _run_once() ->self._ready队列中的所有事件
  二、事件的生成过程
  1、使用asyncio/selector_events.py文件中BaseSelectorEventloop,调用其中的_make_self_pipe函数，然后调用socket.socketpair()创建出两个已连接的socket对象
  参考文件：https://www.cnblogs.com/lijinlei521/p/12707815.html
  2、BaseSelectorEventLoop继承自asyncio/base_events.py中的BaseEvent类。
  2、然后调用_add_reader函数
  3、然后将对应的socket注册到epoll事件循环中监听事件，注意这里还将callback函数封装成了asyncio/events.py中的Handle对象
  4、最后调用生成上下文context = contextvars.copy_context()之后使用context.run()调度对应的函数。
  5、使用BaseEventLoop中的call_soon/call_later/call_at等函数将对应的事件添加到调度循环中，并将事件封装为asyncio/events.py中TimerHandle对象。

asyncio/futures.py文件中的Future对象的set_result函数，本质是调用loop中的call_soon方法请求loop调用所有的回调函数并将状态置为完成，对于await future这中写法可以参考future源码中的 __await__：
def __await__(self):
    if not self.done():
        self._asyncio_future_blocking = True
        yield self  # This tells Task to wait for completion.
    if not self.done():
        raise RuntimeError("await wasn't used with future")
    return self.result()  # May raise too.
另外需要说明的是，一个类实现了__await__函数即可使用await关键字来等待，另外set_result主要还是为了唤醒selector事件循环，让事件能正常结束。

所谓的transport就是将一些对象封装成socket对象，然后使用sokcet对数据传输。

目前为止，阻塞cpu的方式主要有3中方式：
1、使用线程锁, 如evt = threading.Event(); evt.set()或者cond = threading.Condition(); cond.wait(timeout=timeout)
2、使用协程的Future对象，如future = loop.create_future(); await future
3、使用IO多路复用中的select,如select.select([sock], [], [], timeout=timout), 其中的sock可以使用sock.send(b"\0x00")唤醒，或者在一定时间内未发生事件则继续往下执行。
"""