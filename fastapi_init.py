"""
1、创建项目目录：
mkdir fastapi_demo && cd fastapi_demo && python -m venv venv
2、新建config文件夹并创建config.py
内容如下：
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    FASTAPI_PORT: int = Field(..., gt=1000)

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"

3、在项目根目录下创建.env.local文件
内容如下：
FASTAPI_PORT=8080

4、项目根目录下创建app.py
内容如下：
import decimal
import glob
import importlib
import json
import os
from datetime import datetime
from enum import Enum
from typing import Any

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from starlette.middleware.cors import CORSMiddleware

from config.config import Settings

from config.config import get_redis, init_redis, initiate_database, init_register, Settings
from core.protect.protect_redis import init_redis as init_redis_protect, init_redis_plc
from database.log import db_create_device_log
from config.router_config import RouterTag
from models.system import LoginMode
from utils.validators import filter_admin_router
from utils.tri_color_control import TriColorControl
from wss.wss import router as WssRouter

app = FastAPI()

# # 初始化app实例
# if settings.ENV == "PROD":
#     # 生产关闭swagger
#     app = FastAPI(title=settings.APP_NAME, docs_url=None, redoc_url=None)
# else:
#     app = FastAPI(title=settings.APP_NAME,
#                   openapi_url=f"{settings.API_PREFIX}/openapi.json")

# 设置CORS站点
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)


@app.on_event("startup")
async def start_database():
    await initiate_database()
    # 中位机上电日志记录
    await db_create_device_log("MCS启动", "unknow", "项目启动/重启")
    # 如果为联机模式，则开启中位机注册到上位机
    if Settings().MODE == LoginMode.CLUSTER.value:
        await init_register()
    init_redis()
    init_redis_protect(get_redis())
    await init_redis_plc()
    await TriColorControl.sync_median_status()


class DecEncoder(json.JSONEncoder):
    """处理json序列化时的decimal类型数据"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, Enum):
            return obj.value

        super(DecEncoder, self).default(obj)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """处理模型校验错误"""
    errors = []
    for error in exc.errors():
        err_msg = {
            "loc": list(error.get("loc")) if error.get("loc") else [],
            "msg": error.get("msg"),
            "type": error.get("type")
        }

        if ctx := error.get("ctx"):
            err_msg["ctx"] = json.loads(json.dumps(ctx, cls=DecEncoder))
        errors.append(err_msg)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": errors},
    )


@app.get("/", tags=["Root"])
async def read_root():
    return {
        "message": "Server is running.",
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# 自动路由加载
# 路由文件夹下的所有路由文件
folder_path = "routes"
file_paths = glob.glob(f"{folder_path}/*.py")
for file_path in file_paths:
    # 模块名字
    router_name = os.path.split(file_path)[-1].split(".")[0]
    # 获取tag, 如果路由文件存在但是不在tag里,则不引入该路由模块
    if tag := getattr(RouterTag, router_name.upper(), None):
        # import模块
        router = importlib.import_module(f"{folder_path}.{router_name}").router
        if Settings().MODE == LoginMode.CLUSTER.value and tag == RouterTag.ADMIN.value:
            app.include_router(
                router,
                tags=[tag],
                prefix=f"/{router_name}",
                dependencies=[Depends(filter_admin_router)],
            )
        else:
            app.include_router(
                router,
                tags=[tag],
                prefix=f"/{router_name}",
            )

app.include_router(WssRouter, tags=[RouterTag.WEBSOCKETS])

5、项目根目录下创建main.py
内容如下：
import uvicorn
from config.config import Settings


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=Settings().FASTAPI_PORT,
        # reload=True,
        # log_config=dict_config,
    )
"""
