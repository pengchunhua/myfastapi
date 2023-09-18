import asyncio
import pathlib
import uuid

import uvicorn
from loguru import logger
# logger.disable("")  # 关闭所有loguru的打印, 生产环境默认开启

from config.config import Settings
from core import dict_cofnig


def init_env():
    """初始化环境变量"""
    env_file = pathlib.Path(Settings.Config.env_file)
    if not env_file.exists():
        logger.info(f"初始化环境变量: {env_file}")
        env_file.write_text(
            "DATABASE_URL=mongodb://admin:Hrd_8001@localhost:27017/lms_lihao\n"
            "REDIS_BROKER_URL=redis://:Abc123456!@localhost:6379/10\n"
            "REDIS_BACKEND_URL=redis://:Abc123456!@localhost:6379/11\n"
            "REDIS_STREAM_URL_UPPER=redis://:Abc123456!@192.168.80.113:6379/12\n"
            "REDIS_PLC_URL=redis://:Abc123456!@192.168.61.150:6379/15\n"
            f"secret_key={uuid.uuid4().hex}\n"
            "PYTHONPATH=/\n"
            "FASTAPI_HOST=127.0.0.1\n"
            "FASTAPI_PORT=8080\n"
        )
        return

    env_file_content = env_file.read_text()

    # 新增的环境变量配置，同时修改./config/config.py文件
    if "FASTAPI_PORT=" not in env_file_content:
        env_file_content += "\nFASTAPI_PORT=8080"
        env_file.write_text(env_file_content)


init_env()

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=Settings().FASTAPI_PORT,
        # reload=True,
        log_config=dict_cofnig,
    )
