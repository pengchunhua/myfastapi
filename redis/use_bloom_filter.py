from pybloom_live import ScalableBloomFilter, BloomFilter

# 可自动扩容的布隆过滤器
bloom = ScalableBloomFilter(initial_capacity=100, error_rate=0.001)

url1 = 'http://www.baidu.com'
url2 = 'http://qq.com'

bloom.add(url1)
print(url1 in bloom)
print(url2 in bloom)

url1 = 'http://www.baidu.com'
url2 = 'http://qq.com'
# BloomFilter 是定长的
bf = BloomFilter(capacity=1000)
bf.add(url1)
print(url1 in bf)
print(url2 in bf)
