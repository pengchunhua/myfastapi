# 通过代理的方式可以增加一些权限校验

class Proxy(object):
    def __init__(self, obj):
        self._obj = obj

    def __getattr__(self, name):
        print('getattr:', name)
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr:', name, value)
            setattr(self._obj, name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._obj, name)


class Spam:
    def __init__(self, x):
        self.x = x

    def bar(self, y):
        print('Spam.bar:', self.x, y)


if __name__ == "__main__":
    s = Spam(5)
    p = Proxy(s)
    print(p.x)
    p.bar(8)
    p.x = 58

# 直接代理的方式，远程代理的话可以通过RPC来实现
class Subject:
    def request(self):
        pass


class RealSubject(Subject):
    def request(self):
        print('...RealSubject 真正处理请求...')


class Proxy(Subject):
    def __init__(self):
        self.real = RealSubject()

    def request(self):
        print('...请求之前，参数校验...')
        self.real.request()
        print('...请求之后，记录耗时...')


if __name__ == '__main__':
    proxy = Proxy()
    proxy.request()
