# 简单工厂模式
def func1():
  print(f"funtion name:{func1.__name__}")

def func2():
  print(f"function name:{func2.__name__}")

def factory(type)
  func_dict = {
    "func1": func1,
    "func2": func2
  }
  func = func_dict.get(type)
  if not func:
    raise ValueError
  return func()

if __name__ == "__main__":
  res = factory("func1")

#使用工厂产品类
class Person(object):
    def __init__(self,name):
        self.name=name
    def work(self):
        print('开始工作')
        #直接通过工厂子类获取斧头
        axe=Steel_Axe_Factory().create_axe()
        axe.cut_tree()


#产品抽象类
class Axe(object):
    def __init__(self,name):
        self.name=name
    def cut_tree(self):
        print('%s砍树',self.name)
#工厂具体产品1
class StoneAxe(Axe):
    def cut_tree(self):
        print('石斧砍树')
#工厂具体产品2
class SteelAxe(Axe):
    def cut_tree(self):
        print('铁斧砍树')


#工厂方法模式父类/工厂抽象类
class Factory(object):
    def create_axe(self):
        pass
#工厂子类1
class Stone_Axe_Factory(Factory):
    def create_axe(self):
        return StoneAxe('石头')
#工厂子类2
class Steel_Axe_Factory(Factory):
    def create_axe(self):
        return SteelAxe('铁')

p=Person('ll')
p.work()
