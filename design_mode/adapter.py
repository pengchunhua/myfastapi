# 适配器模式，将需要使用的对象调整为使用者对应的接口

# 适配器目标对象
class Logger:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def log(self, message: str):
        with open(self.file_path, 'a') as file:
            file.write(message + '\n')

# 适配器对象
class FileLoggerAdapter:
    def __init__(self, file: File):
        self.logger = Logger(file.name)

    def log(self, message: str):
        self.logger.log(message)

# 适配器使用对象
class LoggerUser(object):
  def __init__(self, file_path, mode):
    self._file = open(file_path, mode)
    self.logger = FileLoggerAdapter(self._file)

  def log(self, message):
    self.logger.log(message)

if __name__ == "__main__":
  user = LoggerUser('log.txt', 'w')
  user.log("This is a log message")
