import inspect
import time
from redis import StrictRedis

# 注意：执行该脚本前需要设置事件通知开启redis-cli -a Abc123456! config set notify-keyspace-events KEA，这是临时方案，如果要永久方案就需要修改配置后重启
# 参考文档：
# 1、https://www.cnblogs.com/fu-yong/p/9628965.html
# 2、https://zhuanlan.zhihu.com/p/103963089
# 该方案存在的问题：因为redis是惰性删除的，所以时间有可能会有一定的滞后，需要根据具体的业务场景来决定是否使用该方案
redis = StrictRedis.from_url("redis://:Abc123456!@192.168.61.80:6379/10")

class RedisEventListener(object):
    def __init__(self, redis:StrictRedis):
        self.redis = redis
        self.pubsub = self.redis.pubsub()
        self.event_watcher = {}
        self.stop = False

    def add_event_handler(self, event, func):
        """
        绑定事件与处理器
        """
        if not inspect.isfunction(func):
            raise ValueError("回调对象必须是函数")
        self.event_watcher[event] = func

    def mypubsub(self):
        """
        订阅事件
        """
        self.pubsub.psubscribe(**self.event_watcher)

    def stop(self):
        """
        停止事件订阅
        """
        time.sleep(50)
        print("stop listener")
        self.stop = True

    def get_handler(self, event, pattern):
        """
        获取事件对应的处理函数
        """
        return self.event_watcher.get(event) or self.event_watcher.get(pattern)

    def run(self):
        """
        事件订阅处理入口
        """
        while not self.stop:
            message = None
            # 这里要注意为什么不直接用get_message是因为get_message是非阻塞的，对cpu性能冲击较大，所以直接使用parse_response来阻塞
            if resp := self.pubsub.parse_response():
                message = self.pubsub.handle_message(resp, ignore_subscribe_messages=True)
            print(f"message:{message}")

def callback(msg):
    print(f"测试:{msg}")

if __name__ == "__main__":
    redis_watcher = RedisEventListener(redis)
    redis_watcher.add_event_handler("__keyspace@0__:mykey", callback)
    redis_watcher.mypubsub()
    redis_watcher.run()
