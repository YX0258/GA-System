import logging

LOG_NAME   = "运行日志.log"       #日志文件名
LOG_MODE   = "a"                  #读写模式
LOG_FORMAT = "%(asctime)s %(levelname)s: %(message)s"   #输出格式
LOG_LEVEL  = logging.INFO         #日志等级

def log_init():
    logging.basicConfig(filename=LOG_NAME, 
                        filemode=LOG_MODE,               
                        format=LOG_FORMAT, 
                        level=LOG_LEVEL)

'''
log_init()
logging.debug('debug message')
logging.info('info message')
logging.warning('warning message')
logging.error('error message')
logging.critical('critical message')

其他文件
logger.logging.error("...")
'''