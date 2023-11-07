# 使用描述器实现property

class mproperty(object):
    def __init__(self, fget, fset=None, fdel=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        
    def __get__(self, obj, klass):
        return self._fget(obj)
    
    def __set__(self, obj, val):
        if not hasattr(self._fset, '__call__'):
            raise AttributeError("Readonly attribute!")
        self._fset(obj, val)
        
    def __delete__(self, obj):
        if not hasattr(self._fdel, '__call__'):
            raise AttributeError("Can't delete the attribute!")
        self._fdel(obj)

    def setter(self, fset):
        self._fset = fset
        return self
    
    def deleter(self, fdel):
        self._fdel = fdel
        return self


class Apple(object):
    def __init__(self, price=0):
        self._price = price
    
    @mproperty
    def price(self):
        return self._price
    
    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price must be greater than 0")
        self._price = value
    
    @price.deleter
    def price(self):
        print("delete price")
