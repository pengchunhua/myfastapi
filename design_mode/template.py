"""Template Pattern with Python Code
"""

from abc import abstractmethod, ABCMeta


class AbstractSort(metaclass=ABCMeta):
    """将数组array由小到大排序
        @param array
    """
    @abstractmethod
    def sort(self, array):
        pass

    def show_sort_result(self, array):
        self.sort(array);
        print("排序结果：");
        for i in range(len(array)):
            print("%3s" % array[i])


class ConcreteSort(AbstractSort):
    def _select_sort(self, array, index):
        MinValue = 32767 # 最小值变量
        indexMin = 0     # 最小值索引变量
        for i in range(index, len(array)):
            if array[i] < MinValue: # 找到最小值
                MinValue = array[i] # 储存最小值
                indexMin = i 
        Temp = array[index] # 交换两数值
        array[index] = array[indexMin]
        array[indexMin] = Temp

    def sort(self, array):
        for i in range(len(array)):
            self._select_sort(array, i)


class Client(object):
    def main(self):
        a = [10, 32, 1, 9, 5, 7, 12, 0, 4, 3] # 预设数据数组
        s = ConcreteSort()
        s.show_sort_result(a)


if __name__ == "__main__":
    Client().main()
