# -*- coding: utf-8 -*-
import sys
import time
import psutil   #需要安装 pip install psutil
import logging
from server_proc import read_proc_info
from server_logger import log_init


# The script starts here
if __name__ == "__main__":
    log_init()
    Proc_Info = {}
    
    #while psutil.pid_exists(pid):
    while True:
        
        Proc_Info = read_proc_info()
        print(Proc_Info)
        '''
        print("进程名称：", proc_info["name"])
        print("进程pid：", proc_info["pid"])
        print("CPU占比：", proc_info["cpu_percent"])
        '''
        print("6666")
        #print("总cpu = ", process.get_cpu_percent())
        #print("总内存 = ", psutil.virtual_memory().percent)
        time.sleep(1)
    else:
        print("进程已关闭")

