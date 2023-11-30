from fastapi import Request

class MyMiddleware:
    def __init__(
            self,
            some_attribute: str,
    ):
        self.some_attribute = some_attribute

    async def __call__(self, request: Request, call_next):
        # do something with the request object
        content_type = request.headers.get('Content-Type')
        print(content_type)
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response

from fastapi import FastAPI
from middleware import MyMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()
my_middleware = MyMiddleware(some_attribute="some_attribute_here_if_needed")
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)




# ===============================另外一种实现方式===============================
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            some_attribute: str,
    ):
        super().__init__(app)
        self.some_attribute = some_attribute

    async def dispatch(self, request: Request, call_next):
        # do something with the request object, for example
        content_type = request.headers.get('Content-Type')
        print(content_type)
        
        # process the request and get the response    
        response = await call_next(request)
        
        return response

  from fastapi import FastAPI
from middleware import MyMiddleware

app = FastAPI()
app.add_middleware(MyMiddleware, some_attribute="some_attribute_here_if_needed")
