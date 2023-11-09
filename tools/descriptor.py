"""
你想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。 但是一旦被访问后，你希望结果值被缓存起来，不用每次都去计算。
__get__(self, instance, owner)
当我们希望获取描述符的值时, 该方法会被调用. 方法参数解释如下:

self : 表示 descriptor 对象本身

instance : 当 descriptor 被实例调用时, 表示该实例, 如果是被类调用, 则该参数为 None

owner : 表示 instance 参数的所属的类

因为 descriptor 是作为类的属性存在的, 所以是可以通过 ClientClass.descriptor 这种方式调用的. __get__ 的接口会看起来显得如此奇怪的原因就是为了保证不管是通过实例调用(obj.descriptor)还是通过类调用(Class.descriptor) , 该接口都能正常工作.

通常来说, 除非我们希望对 owner 进行一些操作, 否则当 instance 为 None 时, 一般返回描述符本身比较好.

__set__(self, instance, value)
当我们对描述符进行赋值操作时, 该方法会被调用. self 参数和 instance 参数同前, value 参数则表示被赋值的具体值.

当我们通过 client.descriptor = "value" 这样的调用方式对描述符进行赋值时, 如果描述符定义了 __set__ 方法,则会调用描述符的 __set__ 方法进行赋值, 此时 value 参数被设为 “value” . 如果描述符没有定义 __set__ 方法,那么 client.descriptor 会被直接覆盖为字符串 “value”. 因此在对描述符进行赋值时,确保该描述符实现了 __set__ 方法.

__delete__(self, instance)
当调用 del 语句从实例中删除描述符时, 该方法会被调用. 例如 del client.descriptor .

__set_name__(self, owner, name)
当我们在一个Class中使用描述符时,我们需要在实例化该描述符时传入该属性的名字. Python 3.6 之前, 这个名字都是通过初始化的时候手动传入的.
"""

class lazyproperty:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value


import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazyproperty
    def area(self):
        print('Computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('Computing perimeter')
        return 2 * math.pi * self.radius


######################################property的两种使用方式#################################
class A:
    def __init__(self, name, score):
        self.name = name # 普通属性
        self.score = score
        
    def getscore(self):
        return self._score
    
    def setscore(self, value):
        print('setting score here')
        if isinstance(value, int):
            self._score = value
        else:
            print('please input an int')
            
    score = property(getscore, setscore)

class A:
    def __init__(self, name, score):
        self.name = name # 普通属性
        self.score = score
        
    @property
    def score(self):
        print('getting score here')
        return self._score
    
    @score.setter
    def score(self, value):
        print('setting score here')
        if isinstance(value, int):
            self._score = value
        else:
            print('please input an int')



#######################################property的实现方式#####################################
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
