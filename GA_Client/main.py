import sys
import socket
import logger
import threading
from readconfig import read_config 
from json import loads,dumps
from process import read_proc_info
from select import select
from time import sleep,time
from ConnectServer import connect_server
'''
#SERVER_HOST = "192.168.0.147"
SERVER_HOST = "192.168.0.199"
SERVER_POST = 8080
'''
config = {}
count = 0

##################################################################
def client_select(config):
    server_ip    = config["host"]
    server_port  = int(config["port"])
    reconn_count = 5

    sock = connect_server(server_ip, server_port, reconn_count)

    event_list   = [sock]
    #pending_list = []              # 存放准备 写入 的客户端套接字
    sock_lock = threading.Lock()    # 创建线程锁，防止sock被关闭

    # 读取服务器发来的数据
    def read_thread():
        nonlocal sock
        time_out = 10               # select() 超时时间 
        while True:
            readable, _, _ = select(event_list, [], [], time_out)
            if readable:
                try:
                    sock_lock.acquire()     # 申请线程锁
                    if not sock:
                        sock_lock.release() 
                    data = sock.recv(1024)
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
            sock.sendall(bytes(serialized_data,"utf-8"))
        except ConnectionAbortedError as err:
            print("服务器主动断开了连接:", err)
            logger.logging.error(err)
            sock = connect_server(server_ip, server_port, reconn_count)
    
    # 定时发送数据
    def send_tasks():
        timing = float(config["send_interval"])
        t = threading.Timer(timing,read_proc_info_task)
        t.setDaemon(True)
        t.start()

    # 读取进程信息
    def read_proc_info_task():
        global count
        Proc_Info = read_proc_info()
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
    # 清理socket，同样道理，这里需要锁定和解锁
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
    client_select(config)

    while True:
        print("主线程正在运行...")
        sleep(20)