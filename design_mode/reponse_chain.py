# 抽象DNS服务父类
class AbstractDnsServer:
    __next_server = None  # 下一级
 
    def resolve(self, domain):
        pass
 
    def set_next(self, next_server):
        self.__next_server = next_server
 
    def get_next(self):
        return self.__next_server
 
 
# 本地hosts
class HostsDnsServer(AbstractDnsServer):
    def resolve(self, domain):
        if random.random() < 0.5:
            print('本地hosts解析')
            return '115.28.87.149'
        else:
            return self.get_next().resolve(domain)
 
 
# 局域网dns服务器
class LANDnsServer(AbstractDnsServer):
    def resolve(self, domain):
        if random.random() < 0.5:
            print('局域网dns服务器解析')
            return '115.28.87.149'
        else:
            return self.get_next().resolve(domain)
 
 
# 根dns服务器
class RootDnsServer(AbstractDnsServer):
    def resolve(self, domain):
        print('dns根服务器解析')
        return '115.28.87.149'

if __name__ == '__main__':
    hostsDnsServer = HostsDnsServer()
    lanDnsServer = LANDnsServer()
    rootDnsServer = RootDnsServer()
 
    hostsDnsServer.set_next(lanDnsServer)
    lanDnsServer.set_next(rootDnsServer)
 
    for i in range(3):
        ip = hostsDnsServer.resolve("www.f2boy.com")
        print('解析结果', ip)
        print()
