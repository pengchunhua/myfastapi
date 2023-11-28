import sys
import urllib.request

def audit_hook(event, args):
    # 事件处理函数
    print(f"event: {event=}")
    if event in ['urllib.Request']:
        print(f"Network, {event=}, {args=}")
      
# 增加事件处理器
sys.addaudithook(audit_hook)


if __name__ == "__main__":
    # 事件生成及触发
    sys.audit("hello")
