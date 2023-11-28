import sys
import time
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from logs import logger


class Data:

    def __init__(self):
        self.driver = webdriver.Firefox()
        logger.info('__init__')
        sys.excepthook = self.HandleException

    def __Sendkeys__(self, Xpath, keys):
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, Xpath)))  # 显示等待      
        self.driver.find_element_by_xpath(Xpath).send_keys(keys)        
            
    def __Click__(self, Xpath):
        WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.XPATH, Xpath)))  # 显示等待
        self.driver.find_element_by_xpath(Xpath).click()

    def Run(self):
        self.driver.get("http://localhost:8080/login/")  
        time.sleep(0.5)  # 强制等待看页面显示结果
        self.__Sendkeys__("//input[@id='user']", "username")
        self.__Sendkeys__("//input[@id='psw']", "password")
        self.__Click__("//*[@id='btn']")
        logger.info('操作成功')
        time.sleep(0.5)
        self.driver.quit()

    def HandleException(self, excType, excValue, tb):
        currentTime = datetime.now() # 时间戳
        logger.info('Timestamp: %s' % (currentTime.strftime("%Y-%m-%d %H:%M:%S")))

        ErrorMessage = traceback.format_exception(excType, excValue, tb)  # 异常信息
        logger.error('ErrorMessage: %s' % ErrorMessage)  # 将异常信息记录到日志中

        logger.error('sys.excepthook: %s' % sys.excepthook)
        logger.error('excType: %s' % excType)
        logger.error('excValue: %s' % str(excValue))
        logger.error('tb: %s' % tb)


if __name__ == "__main__":
    dt = Data()
    dt.Run()
