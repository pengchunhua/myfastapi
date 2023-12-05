"""
python使用文档：
  1、python实现定时器：https://blog.csdn.net/qq_38412868/article/details/100711702
  2、python描述器：https://zhuanlan.zhihu.com/p/52708890
  3、python元类和元类编程：https://zhuanlan.zhihu.com/p/114242597
  4、property实现原理及实现：https://zhuanlan.zhihu.com/p/142029367
  5、python sendfile和mmap(都是为了减少数据在内核空间与用户空间的拷贝，加速系统流程):
    1) os.sendfile实现不同fd之间的数据拷贝：https://pythonjishu.com/python-os-4/
    2) mmap实现进程间通信：https://blog.csdn.net/m0_37422289/article/details/79895526
  6、python实现异步的底层原理是什么：https://www.zhihu.com/question/432814091
  7、python实现简单事件循环：https://zhuanlan.zhihu.com/p/71511434
  8、python signal.set_wakeup_fd的作用和实现：http://timd.cn/python/signal/
  9、python signal的使用方式：https://zhuanlan.zhihu.com/p/91678827
  10、tornado使用signal.set_wakeup_fd的代码：
    1）、https://github.com/tao12345666333/tornado-zh/blob/master/tornado/platform/common.py#L10
    2）、https://github.com/tao12345666333/tornado-zh/blob/master/tornado/ioloop.py
  11、python的信号处理库（事件通知库）：
    1）、https://zhuanlan.zhihu.com/p/435076618
    2）、https://github.com/pallets-eco/blinker/tree/main/src/blinker
  12、linux内核阻塞和异步机制原理：
    1）、https://zhuanlan.zhihu.com/p/461439093
    2）、https://blog.csdn.net/m0_46535940/article/details/124664708
  13、python socket:
    1、https://blog.csdn.net/wowocpp/article/details/115902450
    2、python实现IO多路服用：
      1) https://blog.csdn.net/god_yutaixin/article/details/102791197
      2) https://zhuanlan.zhihu.com/p/367591714
      3) https://www.cnblogs.com/huchong/p/8613308.html
      4) https://blog.csdn.net/xiaomage0511/article/details/122104873
    3、socket连接数(数据是如何分发给对应的函数)：
      1）https://zhuanlan.zhihu.com/p/290651392
      2）https://www.cnblogs.com/sparkleDai/p/7604876.html
      3）https://zhuanlan.zhihu.com/p/165554130
  14、python防死锁方案：
    1） https://python3-cookbook.readthedocs.io/zh-cn/latest/c12/p05_locking_with_deadlock_avoidance.html
  15、python使用pika操作rabbitMQ:
    1) https://www.rabbitmq.com/tutorials/tutorial-one-python.html
  16、python文件锁问题：
    1）https://www.cnblogs.com/itpython/p/10575462.html
    2) fcntl实现进程间的文件锁：https://blog.csdn.net/weixin_45459224/article/details/107669580 和 https://www.cnblogs.com/my_life/articles/7602981.html
  17、python监听鼠标和键盘事件：
    1）、keybord插件监听键盘事件：https://blog.csdn.net/coco56/article/details/107847467
    2）、pynput监听鼠标和键盘事件：https://blog.csdn.net/u011367482/article/details/106173994
  18、事件驱动：
    1）、详解事件驱动event实现：https://blog.csdn.net/brucewong0516/article/details/84031715
  19、SSE服务：
    1、python中实现websocket和SSE实现HTTP:https://blog.csdn.net/weixin_44777680/article/details/114692497
  20、threading中Local类的使用：
    1、threading中Local类的使用：https://blog.csdn.net/brucewong0516/article/details/84589806?spm=1001.2014.3001.5502
  21、asyncio事件循环：
    1）、多线程中启用多个事件循环：
        https://www.jianshu.com/p/29ffdbd65679
        https://www.zhihu.com/question/585648216
    2）、从0到精通事件循环：https://juejin.cn/post/7240427838343577655
  22、python实现RPC框架：https://www.cnblogs.com/wanghuizhao/p/17237670.html
  23、asyncio中的procotol和transport:https://www.jianshu.com/p/e4020e4ea0ba
  24、十六进制与字符串相互转化：https://blog.csdn.net/destiny1507/article/details/100185331
  25、bytearray的转化与解码：
    c = binascii.hexlify(b"hello world")
    d = binascii.unhexlify(c)
    d.encode()
  26、动态配置读取方式：https://zhuanlan.zhihu.com/p/54764686
  注意：所有的远端监听都是通过socket长连接，之后通过本地的queue来实现通知
  27、邮件使用方法：https://blog.csdn.net/xiaolipanpan/article/details/112461566
  28、fastapi中间件实现方式：
    1) https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class
    2) https://www.starlette.io/middleware/
    3) 查看starlette中的middleware源码：from starlette.middleware.base import BaseHTTPMiddleware
  29、Fastapi中的Request生成过程及调用链路：
    ASGI(规范) -> Scope/Receive/Send -> FastApi.__call__() -> starlette.__call__ -> starlette.build_middleware_stack(构建中间件链表) -> 调用接口并返回
    fastapi/FastApi()中的router属性 -> fastapi/routing.py/APIRouter()中的route_class -> fastapi/routing.py/APIRoute() -> starlette/routing.py/routing.Route()中的app属性 -> request_response -> Scope/Receive/Send
  30、DNS相关概念：
    1、https://www.cnblogs.com/bluestorm/p/10345334.html(A记录，MX记录，CNAME记录，NS记录)
    2、python解析DNS:https://www.jianshu.com/p/c8b2175af465
  31、session和requests请求的区别：
    1、https://blog.csdn.net/qq_25986923/article/details/105332640
    2、区别主要是cookies是由用户构建还是由代码直接带入（直接带入已访问的cookie信息则是session, session对象会记录已访问的状态信息，具体可以参考requests/sessions.py/Session对象中的send方法）
    3、认证方式参照：requests/auth.py中的几个类来实现
  32、SSLConnection使用方式（带https的安全认证方式）：
    1、具体参照aioredis/connection.py/SSLConnection及aioredis/connection.py/Connection中的_connect函数
  33、python操作ssh:
    1、https://www.cnblogs.com/wongbingming/articles/12384764.html

java中的参考文档：
  netty能做什么：https://www.zhihu.com/question/24322387
  Java NIO wakeup实现原理：https://www.cnblogs.com/yungyu16/p/13065194.html
  JAVA线程池的7个参数：https://blog.csdn.net/ye17186/article/details/89467919

zookeeper实现分布式锁：
  1、zookeeper入门：https://zhuanlan.zhihu.com/p/98852358
  2、zookeeper架构：https://zhuanlan.zhihu.com/p/108765831
  3、zookeeper服务注册和发现：https://blog.csdn.net/weixin_43866211/article/details/103028284
  4、zookeeper实现分布式锁：
    1） https://www.cnblogs.com/zhaobin022/p/8065317.html
    2） https://zhuanlan.zhihu.com/p/363323742
    3）https://zhuanlan.zhihu.com/p/639756647

redis键空间通知：
  1、键空间通知原理：https://zhuanlan.zhihu.com/p/103963089
  2、键空间通知实现：https://www.cnblogs.com/fu-yong/p/9628965.html
  3、redis常用面试题：https://zhuanlan.zhihu.com/p/276371544
  4、redis的pipeline及transaction:https://www.cnblogs.com/kangoroo/p/7647052.html
  5、redis使用lua脚本：
    1） https://zhuanlan.zhihu.com/p/258890196
    2） https://www.jianshu.com/p/79fb94c4a3a7
  6、redis配置详解：https://www.cnblogs.com/nhdlb/p/14048083.html
  7、redis主从同步：https://zhuanlan.zhihu.com/p/55532249

kafka架构和源码(ISR(存活的副本，主要用于判断ack及主节点的重新选举)/LEO(partion中的最大偏移量，包含未提交到所有副本中的数据)/HW(已提交到所有副本的数据最大偏移量))：
  1、从源码到架构全部讲透：https://zhuanlan.zhihu.com/p/388355017
  2、kafka设计架构详解：https://blog.csdn.net/qq_32828253/article/details/110732652
  3、kafka架构及网络设计原理：https://zhuanlan.zhihu.com/p/95502201
  4、kafka数据持久化机制：https://www.jianshu.com/p/1bdc181a7ebd
  5、kafka的ACK机制：https://juejin.cn/post/7166529283291086879
  6、kafka消费者轮询的准备工作：https://blog.csdn.net/baidu_40468340/article/details/128492534
  7、kafka消费者的消费线程模型：https://zhuanlan.zhihu.com/p/666179914
  8、kafka生产者端线程模型：https://blog.csdn.net/li1669852599/article/details/113694403
  9、深入理解kafka架构：https://zhuanlan.zhihu.com/p/103249714
  10、kafka的事务：https://juejin.cn/post/7122295644919693343
  11、kafka的副本同步机制：https://zhuanlan.zhihu.com/p/473892352

RocketMQ：
  1、图解RocketMQ核心：https://zhuanlan.zhihu.com/p/58892757

rabbimq架构：
  1、rabbitmq整体架构：https://zhuanlan.zhihu.com/p/279392399

Nginx文档：
  1、https://zhuanlan.zhihu.com/p/625184405

Linux性能调优：
  1、https://zhuanlan.zhihu.com/p/470749806
  2、https://blog.csdn.net/xfg0218/article/details/91536066
  3、 https://blog.csdn.net/daocaokafei/article/details/114581983
  4、linux cpu过高问题排查过程：https://blog.csdn.net/fenglibing/article/details/103164183
  5、linux进程的概念：https://zhuanlan.zhihu.com/p/598910454
  6、linux中的cache和buffer:https://zhuanlan.zhihu.com/p/101258495

xxl-job参考文档：
  1、快慢线程池及负载均衡策略：https://blog.csdn.net/qq_35946969/article/details/122567745
  2、分布式任务调度框架：https://zhuanlan.zhihu.com/p/649370118
  3、xxl-job调度中心原理：https://juejin.cn/post/6976412313981026318
  4、XXL-JOB的任务调度执行流程及实现原理：https://blog.csdn.net/qq_38249409/article/details/127494577
  5、xxl-job源码解析类图及架构图：https://blog.csdn.net/Nuan_Feng/article/details/115619448
  6、xxl-job执行器原理：https://juejin.cn/post/6974174691162325028
  说明：在xxl-job中其实executor有两种模式GLUE和执行器模式，其中执行器模式在启动的时候会自动注册到调度中心，后续就可以使用rpc的方式执行并获取执行结果

容器及K8S：
  1、容器镜像打包及迁移：https://blog.csdn.net/qq_14945437/article/details/106135369
  2、k8s用户创建方法：https://www.cnblogs.com/zhaobowen/p/13562487.html
  3、华为云k8s教程：https://support.huaweicloud.com/basics-cce/kubernetes_0010.html
  4、k8s中的service教程：https://blog.csdn.net/Aimee_c/article/details/106964337和https://zhuanlan.zhihu.com/p/157565821
  5、Linux隔离技术-CHROOT:https://zhuanlan.zhihu.com/p/435805234
  6、Linux的NameSpace机制：https://zhuanlan.zhihu.com/p/73248894
  7、Linux Cgroup机制：https://zhuanlan.zhihu.com/p/81668069
  8、Helm教程：https://www.cnblogs.com/zhanglianghhh/p/14165995.html
  9、imagepullSecrets生成及使用：https://blog.csdn.net/Michaelwubo/article/details/108054428
  10、k8s整体架构：https://blog.csdn.net/qq_32476265/article/details/109430317
  11、k8s资源监控：https://zhuanlan.zhihu.com/p/446357481
  12、kubectl及k8s资源监控：https://zhuanlan.zhihu.com/p/561420211
  13、python调用k8s API:https://www.cnblogs.com/linu/p/11703438.html
  14、python通过k8s API实现集群认证：https://blog.csdn.net/anqixiang/article/details/114434578
  
mysql:
  1、InnoDB中的3层B+树能存储多少数据：https://blog.csdn.net/qq_35590091/article/details/107361172
  2、mysql join的底层实现原理：https://www.jianshu.com/p/16ad9669d8a9
  3、mysql锁机制问题：https://zhuanlan.zhihu.com/p/48269420
  4、mysql的两步提交：https://zhuanlan.zhihu.com/p/408175328
  5、mysql高可用集群方案：https://zhuanlan.zhihu.com/p/102798762
  6、mysql锁机制：https://zhuanlan.zhihu.com/p/48269420
  7、mysql配置详细解释：https://developer.aliyun.com/article/822935
  8、mysql整体架构：
    1、https://juejin.cn/post/7143614079532269598
    2、https://juejin.cn/post/7145102393988874253
  9、覆盖索引：https://juejin.cn/post/6844903967365791752

架构模式：
  1、常用的10种架构模式：https://zhuanlan.zhihu.com/p/266696645
  2、架构设计原则：https://zhuanlan.zhihu.com/p/81448795
  
iptables:
  1、iptables四表五链的工作原理：https://zhuanlan.zhihu.com/p/347754874
  2、iptables的SNAT/DNAT:https://zhuanlan.zhihu.com/p/429294272
  3、iptables配置了ssh后仍然不能访问：https://www.zhihu.com/question/496138274

Reactor模型：
  1、Twisted基础教程：https://zhuanlan.zhihu.com/p/84036822

PIP源的修改方式：
  1、修改pip默认源：https://zhuanlan.zhihu.com/p/433878383

APT源的修改方式：
  源资料：https://blog.csdn.net/?url=https%3A%2F%2Fblog.csdn.net%2Fc417469898%2Farticle%2Fdetails%2F106412687
  1、修改/etc/apt/source.list之后apt update

elasticsearch资料：
  1、ES官网：https://www.elastic.co/guide/cn/elasticsearch/guide/current/combining-filters.html
  2、

WSL安装和使用方式：
  1、windows安装WSL:https://blog.csdn.net/weixin_44904239/article/details/130820174
  2、WSL WslRegisterDistribution failed错误处理：https://wenmayi.com/post/3231.html
  3、WSL安装过程：http://home.ustc.edu.cn/~ziheng/article/04/
  4、vscode链接WSL:https://www.cnblogs.com/wxdblog/p/17234342.html
  

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

事件监听有两种方式：
1、while循环监听事件是否发生
2、通过中断来判断事件是否发生目前主要有threading中Event、Condition或者socket通过网卡实现硬中断，即向对应的socket发送一个字节的数据即可
另外如果需要本地实现事件通知，在linux环境下使用socket.socketpair()来实现，windows环境只能通过模拟的方式来实现事件通知
对于CS和BS架构的系统，他们先是通过本地的操作系统监听用户的行为，然后通过socket链接将对应的数据发送给服务端，然后服务端响应对应的数据
另外，也可以通过os.pipe()函数来实现管道，并设置管道的参数为非阻塞即可做到，可以使用这样的方式唤醒select.select或者select.poll的事件监听循环，从而执行一些其他的任务，比如心跳检测，一部任务等等
对于异步事件循环本质上也是通过select及socket来实现的，另外异步事件中的锁都是通过futures.Future来暂停，并通过future.set_result来唤醒实现的，异步事件循环中的await、async的起点也是从future开始的。。。
不管是asyncio_timeout还是其它的超时处理都是使用loop.call_later放入到调度循环中，并且将协程设置result或者设置为cancell

注意：对于使用协程实现socket异步，服务端是可以不需要调整，只需要将客户端使用协程连接并使用reader及writer来读取或者发送对应的指令及数据，这样就完成了整个链路数据处理。具体可以参照aioredis的实现。
异步网络io的接收到数据通知入口：asyncio/subprocess.py/SubprocessStreamProtocol/pip_data_receiveved或pipe_connection_lost函数作为入口通知到等待网络返回的函数
异步socket客户端的调用链：asyncio/streams.py/asyncio.open_connection -> streamreader/streamwriter/protocol(绑定reader数据读取信息，并且绑定transport)/transport(writer通过transport发送数据)
-> asyncio.py/base_events.py/create_connection ->asyncio.py/base_events.py/_create_connection_transport -> asyncio/selector_event.py/_SelectorSocketTransport/_make_socket_transport 
-> 调用socket中的连接对应的网口并调用send/sendto等函数

线程池中的线程复用是在线程结束后向queue队列中发送None,直到有值后重新运行。另外线程的任务被封装为_WorkItem对象，获取到对象后直接使用work_item.run()方法即可
客户端的连接池是将数据库服务端连接对象放到queue或者dict中，当需要时直接从queue或dict中直接获取到连接，然后进行处理，在服务端的连接池主要是用于accptor后对不同的连接处理即大家常用的reacotr模型。

在协程中使用多进程上下文相同只能通过调用相同的初始化函数来实现。
2、uvicorn中的重启时通过过一段时间判定是否需要重启然后重启来实现。
"""
