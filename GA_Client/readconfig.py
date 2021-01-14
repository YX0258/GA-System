from configparser import ConfigParser
import os

def read_config():
    file_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "client_config.ini")
    #file_path = os.path.join(os.path.abspath('.'),'config_test.ini')
    config = ConfigParser()
    if not os.path.exists(file_path):
        raise FileNotFoundError("文件未找到。")

    config.read(file_path, encoding="utf-8")
    item = config.items("ServerParam")

    return dict(item)       # 转换成字典格式返回