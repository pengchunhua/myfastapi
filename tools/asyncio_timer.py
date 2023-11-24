# 参考文档：https://zhuanlan.zhihu.com/p/65175411

# asyio/eventloops.py

def get_event_loop():
    global _event_loop
    if _event_loop is None:
        _event_loop = Eventloop()
    return _event_loop


def _complete_eventloop(fut):
    fut._loop.stop()

class Eventloop:

    def __init__(self):
        self._ready = collections.deque()
        self._scheduled = []
        self._current_handle = None
        self._stopping = False

    def call_later(self, delay, callback, *args):
        if not delay or delay < 0:
            self.call_soon(callback, *args)
        else:
            when = time.time() + delay
            time_handle = TimeHandle(when, callback, self, *args)
            self._scheduled.append(time_handle)
            heapq.heapify(self._scheduled)

    def stop(self):
        self._stopping = True  

    def run_once(self):
        if (not self._ready) and self._scheduled:
            while self._scheduled[0]._when <= time.time():
                time_handle = heapq.heappop(self._scheduled)
                self._ready.append(time_handle)
                if not self._scheduled:
                    break
        ntodo = len(self._ready)
        for i in range(ntodo):
            handle = self._ready.popleft()
            handle._run()

    def run_forever(self):
        while True:
            self.run_once()
            if self._stopping:
                break
              
    def add_delay(self, handle):
        if isinstance(handle, DelayHandle):
            self.call_later(handle._delay, handle._callback, *handle._args)
          
    def run_until_complete(self, fut):
        from asyio.asyio.tasks import ensure_task
        future = ensure_task(fut, self)
        future.add_done_callback(_complete_eventloop, future)
        self.run_forever()

    def run_not_complete(self, fut):
        from .tasks import ensure_task
        future = ensure_task(fut, self)
        self.run_forever()


# asyio/handles.py

class Handle():
    .......


class TimeHandle(Handle):

    def __init__(self, when, callback, loop, *args):
        super().__init__(callback, loop, *args)
        self._when = when

    def __hash__(self):
        return hash(self._when)

    def __lt__(self, other):
        return self._when < other._when

    def __le__(self, other):
        if self._when < other._when:
            return True
        return self.__eq__(other)

    def __eq__(self, other):
        return self._when == self._when

    def __gt__(self, other):
        return self._when > other._when

    def __ge__(self, other):
        if self._when > other._when:
            return True
        return self.__eq__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

class DelayHandle(Handle):

    def __init__(self, delay, callback, loop, *args):
        super().__init__(callback, loop, *args)
        self._delay = delay


# asyio/tasks.py
from .asyio import set_future_result, Future

def _schedule_task(delay, gen, *args):
    coro = gen(*args)
    task = ensure_task(coro)
    task.add_delay_callback(delay, _schedule_task, delay, gen, *args)
    task._scheduled = True
    return task

def schedule_task(delay):
    def decorate(func):
        @wraps(func)
        def wrapper(*args):
            return _schedule_task(delay, func, *args)
        return wrapper
    return decorate

def ensure_task(coro_or_future, loop=None):
    if isinstance(coro_or_future, Future):
        return coro_or_future
    else:
        task = Task(coro_or_future, loop)
    return task
  
def sleep(delay, result=None, loop=None):
    if delay == 0:
        yield
        return result
    future = Future(loop=loop)
    future._loop.call_later(delay, set_future_result, future, result)
    return (yield from future)
    
class Task(Future):
    ....
    def _step(self, exc=None):
        try:
            if exc is None:
                result = self._coro.send(None)
            else:
                print('exc ', exc)
                result = self._coro.throw(exc)
        except StopIteration as exc:
            self.set_result(exc.value)
        else:
            if isinstance(result, Future):
                if result._loop is not self._loop:
                    self._loop.call_soon(
                        self._step, RuntimeError('future 与 task 不在同一个事件循环'))
                elif result._blocking:
                    self._blocking = False
                    result.add_done_callback(self._wakeup, result)
                    # 在这个地方为阻塞的 future 添加了 回调函数。
                else:
                    self._loop.call_soon(
                        self._step, RuntimeError('你是不是用了 yield 才导致这个error?')
                    )
            elif result is None:
                self._loop.call_soon(self._step)
            else:
                self._loop.call_soon(self._step, RuntimeError('你产生了一个不合规范的值'))

# asyio/futures.py
def set_future_result(fut, result):
    fut.set_result(result)
  
class Future:
    def __init__(self, loop=None):
        if loop is None:
            self._loop = get_event_loop()
        else:
            self._loop = loop
        self._callbacks = []
        self._delay_callbacks = []
        self.status = self._PENDING
        self._blocking = False
        self._result = None

    def _schedule_callbacks(self):
        for callback in self._callbacks:
            self._loop.add_ready(callback)
        for delay_callback in self._delay_callbacks:
            self._loop.add_delay(delay_callback)
        self._callbacks = []
        self._delay_callbacks = []

    def add_delay_callback(self, delay, callback, *args):
        if self.done():
            self._loop.call_later(delay, callback, self._loop, *args)
        else:
            delay_handle = DelayHandle(delay, callback, self._loop, *args)
            self._delay_callbacks.append(delay_handle)

    def set_result(self, result):
        self.status = self._FINISHED
        self._result = result
        self._schedule_callbacks()

# 使用
import asyio
import time


def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    yield from asyio.sleep(1)
    return x + y


@asyio.schedule_task(3)
def print_sum(x, y):
    print(time.time())
    result = yield from compute(x, y)
    print("%s + %s = %s" % (x, y, result))


loop = asyio.get_event_loop()
loop.run_not_complete(print_sum(1, 9))
