import time
data = {}

def time_it(func):
    def __wrap(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(f"spend time:{time.time()-start}")
        return res
    return __wrap

def cache_fib(n):
        if n in data:
            return data[n]
        result = 0
        if n in [1,2]:
            result = 1
        else:
            result = cache_fib(n-1) + cache_fib(n-2)
        data[n] = result
        return result

def fibonacci(n):
    i,n1,n2 = 0,1,1
    while i < n:
        yield n1
        n1,n2 = n2,n1+n2
        i+=1


def fib(n):
        if n in [1,2]:
            return 1
        else:
            return  fib(n-1) + fib(n-2)

start = time.time()
result = cache_fib(50)
print(f"cache result:{result}, spend time:{time.time()-start}")
start = time.time()
res = fibonacci(50)
result = [i for i in res]
print(f"no cache result:{result}, spend time:{time.time()-start}")
#start = time.time()
#result = fib(50)
#print(f"no cache result:{result}, spend time:{time.time()-start}")
