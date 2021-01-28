import sys
import socket
import logger
import threading
from readconfig import read_config 
from json import loads,dumps
from process import read_proc_info,find_proc
from select import select
from time import sleep,time
from ConnectServer import connect_server
from Device_manager import check_device

config = {}
count = 0
data_packet = {}

##################################################################
def client_select(config):
    server_ip    = config["ServerParam"]["host"]
    server_port  = int(config["ServerParam"]["port"])
    reconn_count = 5

    sock = connect_server(server_ip, server_port, reconn_count)

    event_list   = [sock]
    #pending_list = []              # 存放准备 写入 的客户端套接字
    sock_lock = threading.Lock()    # 创建线程锁，防止sock被关闭

    # 读取服务器发来的数据
    def read_thread():
        nonlocal sock               # 外函数的变量
        time_out = 10               # select() 超时时间 
        while True:
            readable, _, _ = select(event_list, [], [], time_out)
            if readable:
                try:
                    sock_lock.acquire()     # 申请线程锁
                    if not sock:
                        sock_lock.release() 
                    data = sock.recv(1024)
                    if data is "b''":
                        print("服务器已断开，正在重连...")
                    sock_lock.release()

                    print("获取的数据：", data)
                except ConnectionAbortedError as err:
                    logger.logging.error(err)
                    sock = connect_server(server_ip, server_port, reconn_count)
    
    # 发送数据至服务器
    def send_data(data):
        nonlocal sock
        serialized_data = dumps(data)       # 序列化数据，转换成JSON格式
        try:
            print("数据长度：", len(serialized_data))
            sock.sendall(bytes(serialized_data,"utf-8"))
        except socket.error:
            print("服务器主动断开了连接:", socket.error)
            logger.logging.error(socket.error)
            sock = connect_server(server_ip, server_port, reconn_count)
    
    proc_list = find_proc(config["Process"])    # 进程列表

    # 定时发送数据
    def send_tasks():
        timing = float(config["ServerParam"]["send_interval"])
        t = threading.Timer(timing,read_proc_info_task)
        #s = threading.Event()
        t.setDaemon(True)
        t.start()

    # 读取进程信息
    def read_proc_info_task():
        global count
        Proc_Info = read_proc_info(proc_list)
        print(Proc_Info)
        send_data(Proc_Info)     # 发送进程数据
        send_data(count)
        count += 1
        send_tasks()                     # 定期发送

    read_thread = threading.Thread(target=read_thread)
    read_thread.setDaemon(True)     #守护线程,不设置退不出程序
    read_thread.start()
    send_tasks()

'''
    # 关闭socket，锁定和解锁
    sock_lock.acquire()
    sock.close()
    sock = None
    sock_lock.release()
'''

##################################################################

# The script starts here
if __name__ == "__main__":    
    logger.log_init()

    config = read_config()  
    '''
    server_config = config["ServerParam"]
    process_config = config["Process"]
    '''
    # client_select(server_config)

    client_select(config)

    while True:
        disconn_dev = check_device(config["Device"], 0)
        print("主线程正在运行，检测设备是否接入...")
        print("未连接设备：", disconn_dev)
        sleep(3)