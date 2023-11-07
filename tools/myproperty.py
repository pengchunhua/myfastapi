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


# 另外的实现
class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)
