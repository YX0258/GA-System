import os
import psutil
import datetime
from server_logger import logging

proc_dict = {
    #"name"        :"Calculator.exe",
    "name"        : "notepad.exe",  #进程名称
    "pid"         : None,           #进程PID
    "cpu_percent" : 0,              #进程CPU使用率 %
    "mem_percent" : 0,              #进程内存使用率 %
    "cup_used"    : 0,              #已使用的总cpu %
    "mem_used"    : 0.00,              #已使用的总内存 %
    "cpu_limit"   : 50,             #进程最大CPU限制
    "mem_limit"   : 50,             #进程最大内存限制
    "path"        :"C:/Users/GA2/Desktop/Python/project/test/路径测试.txt"  #文件路径
}

#获取CPU占比
def get_cpu_percent():
    return psutil.cpu_percent(interval=None)   #检测间隔

#获取内存占比
def get_mem_percent():  
    return psutil.virtual_memory().percent

#根据进程名称获得pid
def get_pid_by_name(str_proc_name):
    for proc in psutil.process_iter():      #查找目标进程
        if proc.name() == str_proc_name:    
            print("找到目标进程")
            return proc.pid
    return 0

#打开指定路径的文件（程序），并返回该进程pid
def process_open(path):
    os.startfile(path)
    return get_pid_by_name(proc_dict["name"])

#获取进程详细信息，存放到 proc_dict 字典中
def get_proc_info(proc_pid):

    if proc_pid == None:    #初次运行
        proc_dict["pid"] = process_open(proc_dict["path"])  #自动打开文件
        proc_pid = get_pid_by_name(proc_dict["name"])
    
    while True:     
        try:
            proc = psutil.Process(proc_pid)
            proc_dict["pid"]         = proc_pid
            proc_dict["name"]        = proc.name()
            proc_dict["mem_percent"] = proc.memory_percent()
            proc_dict["cpu_percent"] = proc.cpu_percent(interval=None) 
            proc_dict["cup_used"]    = get_cpu_percent()
            proc_dict["mem_used"]    = get_mem_percent()
            break
        except psutil.NoSuchProcess as errmsg:  #读取过程中异常关闭
            print(errmsg)
            proc_dict["pid"] = process_open(proc_dict["path"])  #重新打开进程
            proc_pid = proc_dict["pid"]
            ###############
            #输出值错误日志
            logging.warning(errmsg)
            ###############

'''
#根据pid获取进程信息
def get_proc_info(proc_pid):
    proc_info = {}

    try:
        proc = psutil.Process(proc_pid)
        proc_info["pid"]         = proc_pid
        proc_info["name"]        = proc.name()
        proc_info["mem_percent"] = proc.memory_percent()
        proc_info["cpu_percent"] = proc.cpu_percent(interval=None)

    except psutil.NoSuchProcess as errmsg:
        print(errmsg)
        #global PID = process_open(FILE_PATH)  #重新打开进程
        proc = psutil.Process(PID)
        proc_info["pid"]         = PID
        proc_info["name"]        = proc.name()
        proc_info["mem_percent"] = proc.memory_percent()
        proc_info["cpu_percent"] = proc.cpu_percent(interval=None) 

    return proc_info
'''


def read_proc_info():

    get_proc_info(proc_dict["pid"]) #获取信息

    proc_info_temp = proc_dict.copy()


    return proc_info_temp

