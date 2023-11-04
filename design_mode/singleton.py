# 单例的3种实现方式

class Singleton(object):
  def __new__(cls, *args, **kwargs):
    if not hasattr(cls, "_instance"):
      cls._instance = super().__new__(cls,*args, **kwargs)
    return cls._instance

def singleton(cls):
  _instance = {}
  def __inner():
    if cls not in _instance:
      _instance[cls] = cls()
    return _instance[cls]
  return __inner

class singleton(object):
  def __init__(self, cls):
    self._cls = cls
    self._instance = {}

  def __call__(self)
    if self._cls not in self._instance:
      self._instance[self._cls] = self._cls()
    return self._instance[self._cls]


    
