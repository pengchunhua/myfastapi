# 参考文档：https://www.cnblogs.com/shuzf/p/17201149.html
import sys

def function():
    x=1
    try:
        assert 1==2
    except Exception as e:
       x=e
    return x

def trace(frame, event, arg):
    """
        frame:frame 是当前堆栈帧
        event:一个字符串，可以是'call', 'line', 'return', 'exception'或者'opcode'
        arg:取决于事件类型

            frame.f_code.co_name  执行函数名称
            frame.f_lineno   执行行号
            frame.f_locals["arr"]
    """
    print(event, frame.f_code.co_name, frame.f_lineno,"==>", frame.f_locals, arg)
    return trace

sys.settrace(trace)
function()
sys.settrace(None)



# ============================================================
import sys
from functools import wraps


def trace_variable(variable_name):
    def decorator(func):
        change_history = []

        def trace(frame, event, arg):
            # value = frame.f_locals.get(variable_name)
            # if value not in change_history:
            #     change_history.append((value))
            print(event, frame.f_code.co_name, frame.f_lineno, frame.f_locals, arg)
            return trace

        @wraps(func)
        def inner(*args, **kwargs):
            sys.settrace(trace)
            result = func(*args, **kwargs)
            sys.settrace(None)
            return result
        return inner
    return decorator


@trace_variable('arr')
def bSort(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


if __name__ == "__main__":
    arr = [3, 2, 1]
    bSort(arr)
