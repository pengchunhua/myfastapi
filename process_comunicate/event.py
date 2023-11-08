import multiprocessing,time,random
def restaurant_handle(event): #餐厅的处理进程
    print("1、【餐厅】为食客安排座位，并在一旁等待食客点餐。。。")
    time.sleep(random.randint(1,3))
    event.set()#解除阻塞状态
    event.clear()#清除已有的状态
    event.wait()#等待食客后续处理

    print("3、【餐厅】厨师接到菜单，开始烹饪美食。。。")
    time.sleep(random.randint(1,3))
    event.set() #解除阻塞状态
    event.clear()  # 之前的状态清空
    event.wait()

    print("5、【餐厅】收银台算正在算账。。。")
    time.sleep(random.randint(1,3))
    event.set()  # 解除阻塞状态
    event.clear()  # 之前的状态清空
    event.wait()

    print("7、【餐厅】收银台收到钱。。。")
    time.sleep(random.randint(1,3))
    event.set()
    event.clear()
    event.wait()

def diners_hangle(event):#食客的处理进程
    event.wait() #等待之前的第一步完成  两个进程所以先阻塞，让另一个执行

    print("2、【食客】食客看完菜单，选好了自己心仪的美食。。。")
    time.sleep(random.randint(1,3))
    event.set() #解除阻塞状态
    event.clear()#之前的状态清空
    event.wait()#继续等待后续的处理步骤

    print("4、【食客】享用丰盛的美食。。。")
    time.sleep(random.randint(1,3))
    event.set()
    event.clear()
    event.wait()

    print("6、【食客】食客吃晚餐走向收银台付款。。。")
    time.sleep(random.randint(1,3))
    event.set()
    event.clear()
    event.wait()

    print("8、【食客】食客离开")
    event.set()

def main():
    event = multiprocessing.Event()#定义一个event同步处理
    restaurant_process = multiprocessing.Process(target=restaurant_handle,args=(event,),name="餐厅服务进程")
    diners_process = multiprocessing.Process(target=diners_hangle,args=(event,),name="食客进程")
    restaurant_process.start()
    diners_process.start()
if __name__ == '__main__':
    main()
