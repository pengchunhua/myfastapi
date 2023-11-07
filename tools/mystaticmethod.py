# 描述器实现mystaticmethod

class mstaticmethod(object):
    def __init__(self, func):
        self._func = func
        
    def __get__(self, obj, klass=None):
        return self._func
    
    @property
    def __func__(self):
        return self._func
    

class Apple(object):  
    def __init__(self, price=0):
        self._price = price
    
    @mstaticmethod
    def kg2jin(weight):
        # 将千克转换为斤
        return weight * 2
