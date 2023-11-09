# 使用zookeeper实现服务注册与发现
# -*- coding: utf-8 -*
import time
import random
import logging
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
from kazoo.client import KazooState
from ..utils.util import ZOOKEEPER_CONFIG
from app.utils.util import HOST_CONFIG
logger = logging.getLogger(__name__)


class ServiceRegister:
    """
    hosts: the connection string for zk server, such as
    '10.0.1.1:2181,10.0.1.2:2181'
    The object should be created after service has been started successfully.
    """
    def __init__(self):
        self._hosts = ZOOKEEPER_CONFIG["zk_server"]
        self._zk_path = ZOOKEEPER_CONFIG["zk_path"]
        self._zk = None
        # self.start_zk()

    def start_zk(self):
        self._info = (
            f'{self._zk_path}/' + HOST_CONFIG["host"] + ':' + HOST_CONFIG["port"]
        )
        self._zk = None
        try:
            self._zk = KazooClient(self._hosts, auth_data=ZOOKEEPER_CONFIG["zk_auth_data"], logger=logger)
            self._zk.start()
        except Exception as start_zk_e:
            logger.error(
                f'Fail to connect to zk hosts {self._hosts}, exception {start_zk_e}'
            )
            self._zk = None
            raise start_zk_e

        def zk_listener(state):
            logger.info('注册 到 zookeeper')
            if state == KazooState.CONNECTED:
                # Handle being connected/reconnected to Zookeeper
                logger.debug('reconnect to zookeeper')
                try:
                    self.start_zk()
                    self.register()
                except Exception as e:
                    logger.error(f'Fail to register info {self._info}, exception {e}')
                    self._zk.stop()
                    self._zk = None
                    time.sleep(5)
            else:
                logger.debug(f'zk_listener state {state}')

        logger.info('add_listener to zookeeper')
        self._zk.add_listener(zk_listener)

    def create_znode(self):
        def retryCreateNode(self):
            print('重试')
            self.register()

        """
        create an ephemeral and not sequence node in root with service info
        :param info: znode info including ip and port
        """
        logger.info('1111')
        try:
            self._zk.ensure_path(self._zk_path)
            path = self._zk.create(self._info,
            value=b"{\'title\':\'test\'}",
            ephemeral=True,
            sequence=False)
            children = self._zk.get_children(self._zk_path, watch=retryCreateNode(self))
            # self._zk.stop
        except Exception as e:
            logger.error(f'Fail to register info {self._info}, exception {e}')
            return False, ""
        return True, path

    def register(self):
        # When worker start, register on zookeeper forever
        logger.info('注册')
        flag = True
        while flag:
            if not self._zk.exists(self._info):
                success, path = self.create_znode()
                if success:
                    flag = False
                    logger.info(f'register on {path}; hosts {self._hosts} end')
                        # zookeeper syncLimit=5
            time.sleep(5)

    def create_zone(self, zone):
        """
        create zone in cluster
        If the zone is already exist, do nothing, else create
        the given zone path.
        """
        try:
            self._zk.create(zone, f'zone of {zone}', makepath=True)
        except NodeExistsError:
            pass
        except Exception as e:
            logger.error(f'Fail to create zone {e}')
            raise e

    def get_zk_children(self, _zk_path):
        try:
            self._zk_path = f'/BD/services/{_zk_path}'
            self._zk = KazooClient(self._hosts, auth_data=ZOOKEEPER_CONFIG["zk_auth_data"], logger=logger)
            self._zk.start()
            if self._zk.exists(self._zk_path):
                children = self._zk.get_children(self._zk_path)
            else:
                return {
                    "success": False,
                    "message": f"{_zk_path}服务获取失败",
                    "data": None,
                    "failed": True,
                }
            return children
        except Exception as e:
            logger.error(f'Fail to get children {e}')
            raise e

    def get_service(self, _zk_path):  # sourcery skip: raise-specific-error
        """
        获取单个服务
        """
        children = self.get_zk_children(_zk_path)
        if not children:
            raise Exception(f"获取zk中的 {_zk_path} 服务失败！")
        choice = random.sample(children, 1)
        result = {
            "success": True,
            "message": f"{_zk_path}服务获取成功",
            "data": f'http://{choice[0]}/',
            "failed": False,
        }
        self._zk.stop()
        return result

    def get_services(self, _zk_path, k=0):
        """
        获取多个服务，k为获取指定数量的服务
        如果k为0或者为None 则返回目录下全部服务
        """
        children = self.get_zk_children(_zk_path)
        if not k or k > len(children):
            k = len(children)
        choice = random.sample(children, k)
        data = [f'http://{item}/' for item in choice]
        result = {
            "success": True,
            "message": f"{_zk_path}服务获取成功",
            "data": data,
            "failed": False,
        }
        self._zk.stop()
        return result

    def is_slave(self):
        return not self.is_master
