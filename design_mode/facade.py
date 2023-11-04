"""
步骤1：定义子系统，即三个子元件：一个警报器，一个喷水器，一个自动拨打电话的装置
"""
class AlarmSender(object):
    def run(self, msg):
        return "产生了高温告警: {}".format(msg)
 
class WaterSprinker(object):
    def run(self):
        return "洒水降温"
 
class Dialer(object):
    def run(self, name, phone):
        return "拨打值班人：{} 电话: {}".format(name, phone)
 
"""
步骤二：定义外观类，封装子系统的操作
"""
class EmergencyFacade(object):
    def __init__(self):
        self.alarm = AlarmSender()
        self.water = WaterSprinker()
        self.dialer = Dialer()
 
    def run(self, name, phone, msg):
        data = []
        data.append(self.alarm.run(msg))
        data.append(self.water.run())
        data.append(self.dialer.run(name, phone))
        return data
 
if __name__ == "__main__":
    name = "Bruce"
    phone = "210-123456"
    msg = "高温告警，请立即处理"
    emergency = EmergencyFacade()
    resp = emergency.run(name, phone, msg)
    print(resp)
