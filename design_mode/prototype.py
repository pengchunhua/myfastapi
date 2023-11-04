from copy import copy, deepcopy

class Prototype(object):
    """
    　　　设计一个图层对象，用background表示背景的RGBA，简单用content表示内容，除了直接绘画，还可以设置透明度。
　　"""
  def __init__(self):
    self.background=[0,0,0,0]
    self.content="blank"
    
  def getContent(self):
      return self.content
    
  def getBackground(self):
      return self.background
    
  def paint(self,painting):
      self.content=painting
    
  def setParent(self,p):
      self.background[3]=p
    
  def fillBackground(self,back):
      self.background=back
    
  def clone(self):
      return copy(self)
    
  def deep_clone(self):
      return deepcopy(self)

if __name__ == "__main__":
  a = Prototype()
  b = a.deep_clone()
