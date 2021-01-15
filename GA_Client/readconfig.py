from configparser import ConfigParser
from os import path

# 读取配置文件的所有键和值，以字典形式返回
def read_config():
    file_path = path.join(path.split(path.realpath(__file__))[0], "client_config.ini")
    config = ConfigParser()
    if not path.exists(file_path):
        raise FileNotFoundError("文件未找到。")
    
    config.read(file_path, encoding="utf-8")

    item = {}
    section = config.sections()
    for s in section:
        item.update(dict(config.items(s)))

    return item