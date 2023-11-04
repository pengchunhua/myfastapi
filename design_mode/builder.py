# 建造者模式与策略模式的区别是，建造者提供能实现的功能，direcotr指挥实施
# 策略模式则是完成所有的功能，对调用提供完整的功能

class HotelBuilder:
    @classmethod
    def get_material(cls):
        print("正在搬运酒店建筑材料...")
        return cls

    @classmethod
    def building(cls):
        print("正在修建酒店...")
        return cls

    @classmethod
    def complete(cls):
        print("修建酒店已完工")
        return "酒店

class Director:
    def __init__(self, builder):
        self.builder = builder

    def direct(self):
        building = self.builder.get_material().building().complete()
        print(f"{building}已建成")
        return building

if __name__ == "__main__":
  hotel = Director(HotelBuilder).direct()
