from os import startfile
import psutil
import logger
'''
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
    startfile(path)
    return get_pid_by_name(proc_dict["name"])

#获取进程详细信息，存放到 proc_dict 字典中
def get_proc_info(proc_pid):

    if proc_pid == None:    #初次运行
        proc_dict["pid"] = process_open(proc_dict["path"])  #自动打开文件
        proc_pid = get_pid_by_name(proc_dict["name"])
'''
#######################################################################################
def get_pid_fname(name, path):
    temp_list = []
    for proc in psutil.process_iter():                  # 查找目标进程
        if proc.name() == name:
            cwd = proc.cmdline()[len(proc.cmdline())-1] # 获取命令行
            if cwd.find(path) == 0:                     # 从命令行里找路径
                proc_dict = {
                    "name"  : name,
                    "pid"   : proc.pid,                 # 获取PID
                    "fname" : cwd.lstrip(path)          # 从命令行截取文件名
                }
                temp_list.append(proc_dict)             # 添加进列表
                
    return temp_list

# 从设备管理器寻找配置文件里的进程，每个进程创建一个dict，存进列表并返回
def find_proc(config_proc):
    proc_list = []
    proc_name = ""
    proc_path = ""
    
    for p in config_proc:
        if proc_name == "":
            proc_name = config_proc[p]
        else:
            proc_path = config_proc[p]
            temp_list = get_pid_fname(proc_name, proc_path)
            if temp_list == []:   # 进程没运行
                print("没有找到进程“%s”,请检查是否已经运行" % proc_name)
            else:
                proc_list.extend(temp_list)
            proc_name = ""
    return proc_list

def get_other_info(proc_pid):
    try:
        proc = psutil.Process(proc_pid)
        mem_percent = proc.memory_percent()             # 进程内存占用
        cpu_percent = proc.cpu_percent(interval=None)   # 进程CPU占用
        proc_status = proc.status()
        
    except psutil.NoSuchProcess as errmsg:  #读取过程中异常关闭
        print(errmsg)
        #proc_dict["pid"] = process_open(proc_dict["path"])  #重新打开进程
        #proc_pid = proc_dict["pid"]
        #logger.logging.warning(errmsg)
        return 0
    else:
        add_info = {
            "mem_percent" : round(mem_percent, 2),
            "cpu_percent" : round(cpu_percent, 2),
            "proc_status" : proc_status
        }
        return add_info

# 根据进程列表，获取进程的其他信息
def read_proc_info(proc_list):
    for p in proc_list:
        temp_info = get_other_info(p["pid"])
        if temp_info == 0:
            proc_list.remove(p)     # 从列表中移除     
        else:
            p.update(temp_info)     # 根据PID获取其他信息
    return proc_list                # 返回新的信息列表

########
'''
调用方法：
proc_list = find_proc(process_config)   # 通过配置文件获得需要监测的进程列表
proc_dict = read_proc_info(proc_list)   # 读取详细进程信息，返回列表，元素为每个进程的信息字典
'''
########