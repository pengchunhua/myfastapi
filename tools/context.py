import contextlib

@contextlib.contextmanager
def open_func(file_name):
    # __enter__方法
    print('open file:', file_name, 'in __enter__')
    file_handler = open(file_name, 'r')
	
    # 【重点】：yield
    yield file_handler

    # __exit__方法
    print('close file:', file_name, 'in __exit__')
    file_handler.close()
    return

with open_func('/Users/MING/mytest.txt') as file_in:
    for line in file_in:
        print(line)


# 上下文协议器的实现
class Resource():
    def __enter__(self):
        print('===connect to resource===')
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('===close resource connection===')
        
    def operate(self):
        print('===in operation===')
        
with Resource() as res:
    res.operate()
