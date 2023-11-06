# ==============================线程事件驱动管理器======================================

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 13:51:31 2018

@author: 18665
"""
# 系统模块
from queue import Queue, Empty
from threading import *
########################################################################
class EventManager:
    #----------------------------------------------------------------------
    def __init__(self):
        """初始化事件管理器"""
        # 事件对象列表
        self.__eventQueue = Queue()
        # 事件管理器开关
        self.__active = False
        # 事件处理线程
        self.__thread = Thread(target = self.__Run)
        self.count = 0
        # 这里的__handlers是一个字典，用来保存对应的事件的响应函数
        # 其中每个键对应的值是一个列表，列表中保存了对该事件监听的响应函数，一对多
        self.__handlers = {}
    #----------------------------------------------------------------------
    def __Run(self):
        """引擎运行"""
        print('{}_run'.format(self.count))
        while self.__active == True:
            try:
                # 获取事件的阻塞时间设为1秒
                event = self.__eventQueue.get(block = True, timeout = 1)  
                self.__EventProcess(event)
            except Empty:
                pass
            self.count += 1
    #----------------------------------------------------------------------
    def __EventProcess(self, event):
        """处理事件"""
        print('{}_EventProcess'.format(self.count))
        # 检查是否存在对该事件进行监听的处理函数
        if event.type_ in self.__handlers:
            # 若存在，则按顺序将事件传递给处理函数执行
            for handler in self.__handlers[event.type_]:
                handler(event)
        self.count += 1
    #----------------------------------------------------------------------
    def Start(self):
        """启动"""
        print('{}_Start'.format(self.count))
        # 将事件管理器设为启动
        self.__active = True
        # 启动事件处理线程
        self.__thread.start()
        self.count += 1
    #----------------------------------------------------------------------
    def Stop(self):
        """停止"""
        print('{}_Stop'.format(self.count))
        # 将事件管理器设为停止
        self.__active = False
        # 等待事件处理线程退出
        self.__thread.join()
        self.count += 1
    #----------------------------------------------------------------------
    def AddEventListener(self, type_, handler):
        """绑定事件和监听器处理函数"""
        print('{}_AddEventListener'.format(self.count))
        # 尝试获取该事件类型对应的处理函数列表，若无则创建
        try:
            handlerList = self.__handlers[type_]
        except KeyError:
            handlerList = []
			self.__handlers[type_] = handlerList
        # 若要注册的处理器不在该事件的处理器列表中，则注册该事件
        if handler not in handlerList:
            handlerList.append(handler)
        print(self.__handlers)
        self.count += 1
    #----------------------------------------------------------------------
    def RemoveEventListener(self, type_, handler):
        """移除监听器的处理函数"""
        print('{}_RemoveEventListener'.format(self.count))
        try:
            handlerList = self.handlers[type_]
            # 如果该函数存在于列表中，则移除
            if handler in handlerList:
                handlerList.remove(handler)
            # 如果函数列表为空，则从引擎中移除该事件类型
            if not handlerList:
                del self.handlers[type_]
        except KeyError:
            pass
        self.count += 1
    #----------------------------------------------------------------------
    def SendEvent(self, event):
        """发送事件，向事件队列中存入事件"""
        print('{}_SendEvent'.format(self.count))
        self.__eventQueue.put(event)
        self.count += 1
########################################################################
"""事件对象"""
class Event:
    def __init__(self, type_=None):
        self.type_ = type_      # 事件类型
        self.dict = {}          # 字典用于保存具体的事件数据




# ===========================================测试代码===============================================
# encoding: UTF-8
import sys
from datetime import datetime
from threading import *
#sys.path.append('D:\\works\\TestFile')
#print(sys.path)
from eventManager import *

#事件名称  新文章
EVENT_ARTICAL = "Event_Artical"

#事件源 公众号
class PublicAccounts:
    def __init__(self,eventManager):
        self.__eventManager = eventManager

    def WriteNewArtical(self):
        #事件对象，写了新文章
        event = Event(type_=EVENT_ARTICAL)
        event.dict["artical"] = u'如何写出更优雅的代码\n'
        
        #发送事件
        self.__eventManager.SendEvent(event)
        print(u'公众号发送新文章\n')

#监听器 订阅者
class Listener:
    def __init__(self,username):
        self.__username = username

    #监听器的处理函数 读文章
    def ReadArtical(self,event):
        print(u'%s 收到新文章' % self.__username)
        print(u'正在阅读新文章内容：%s'  % event.dict["artical"])

"""测试函数"""
#--------------------------------------------------------------------
def test():
    # 实例化监听器
    listner1 = Listener("thinkroom") #订阅者1
    listner2 = Listener("steve")     #订阅者2
    # 实例化事件操作函数
    eventManager = EventManager()

    #绑定事件和监听器响应函数(新文章)
    eventManager.AddEventListener(EVENT_ARTICAL, listner1.ReadArtical)
    eventManager.AddEventListener(EVENT_ARTICAL, listner2.ReadArtical)
    # 启动事件管理器,# 启动事件处理线程
    eventManager.Start()

    publicAcc = PublicAccounts(eventManager)
    timer = Timer(2, publicAcc.WriteNewArtical)
    timer.start()

if __name__ == '__main__':
    test()

