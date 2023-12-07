from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yoyo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

# 校验异常统一处理入口
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """处理模型校验错误"""
    errors = []
    for error in exc.errors():
        err_msg = {"loc": list(error.get("loc")) if error.get("loc") else []}
        err_msg["msg"] = error.get("msg")
        err_msg["type"] = error.get("type")

        if ctx := error.get("ctx"):
            err_msg["ctx"] = json.loads(json.dumps(ctx, cls=DecEncoder))
        errors.append(err_msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"deatil": errors},
    )

