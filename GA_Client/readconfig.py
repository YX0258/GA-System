from configparser import ConfigParser
from os import path

# 读取配置文件信息，返回字典
def read_config():
    file_path = path.join(path.split(path.realpath(__file__))[0], "client_config.ini")
    config = ConfigParser()
    if not path.exists(file_path):
        raise FileNotFoundError("文件未找到。")
    
    config.read(file_path, encoding="utf-8")

    section_dict = {}
    section = config.sections()

    for s in section:
        section_dict[s] = {}
        section_dict[s].update(dict(config.items(s)))

    return section_dict