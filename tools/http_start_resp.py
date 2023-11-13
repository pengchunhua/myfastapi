# 所有的http入口均为该函数，可以在函数的入口增加中间件，实现自定义处理方法
import os, sys

enc, esc = sys.getfilesystemencoding(), 'surrogateescape'

def unicode_to_wsgi(u):
    # Convert an environment variable to a WSGI "bytes-as-unicode" string
    return u.encode(enc, esc).decode('iso-8859-1')

def wsgi_to_bytes(s):
    return s.encode('iso-8859-1')

def run_with_cgi(application):
	# 按照WSGI协议，构建environ内容
	# 1类 CGI相关的变量，此脚本就是用于cgi执行，所以前面的web服务器已经将CGI变量封装好，这里直接使用
    environ = {k: unicode_to_wsgi(v) for k,v in os.environ.items()}
    # 2类 wsgi定义的变量
    environ['wsgi.input']        = sys.stdin.buffer
    environ['wsgi.errors']       = sys.stderr
    environ['wsgi.version']      = (1, 0)
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True

    if environ.get('HTTPS', 'off') in ('on', '1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set = []
    headers_sent = []

    def write(data):
	    # 将内容返回
        out = sys.stdout.buffer

        if not headers_set:
             raise AssertionError("write() before start_response()")

        elif not headers_sent:
             # Before the first output, send the stored headers
             status, response_headers = headers_sent[:] = headers_set
             out.write(wsgi_to_bytes('Status: %s\r\n' % status))
             for header in response_headers:
                 out.write(wsgi_to_bytes('%s: %s\r\n' % header))
             out.write(wsgi_to_bytes('\r\n'))

        out.write(data)
        out.flush()
	
	
    def start_response(status, response_headers, exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[1].with_traceback(exc_info[2])
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status, response_headers]

        # Note: error checking on the headers should happen here,
        # *after* the headers are set.  That way, if an error
        # occurs, start_response can only be re-called with
        # exc_info set.

        return write
	
	# 将上面处理的参数交给应用程序
    result = application(environ, start_response)
    try:
	    # 将请求到的结果写回。
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result, 'close'):
            result.close()


# 中间件方式实现
import time
from wsgiref.simple_server import make_server

class ResponseTimingMiddleware(object):
    """记录请求耗时"""
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        start_time = time.time()
        response = self.app(environ, start_response)
        response_time = (time.time() - start_time) * 1000
        timing_text = "记录请求耗时中间件输出\n\n本次请求耗时: {:.10f}ms \n\n\n".format(response_time)
        response.append(timing_text.encode('utf-8'))
        return response

def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, response_headers)
    
    return_body = []
    
    for key, value in environ.items():
        return_body.append("{} : {}".format(key, value))
    
    return_body.append("\nHello WSGI!")
    # 返回结果必须是bytes
    return ["\n".join(return_body).encode("utf-8")]

# 创建应用程序
app = ResponseTimingMiddleware(simple_app)
# 启动服务，监听8080
httpd = make_server('localhost', 8080,  app)  
httpd.serve_forever()
