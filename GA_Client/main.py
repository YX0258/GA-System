import sys
import socket
import threading
from readconfig import read_config 
from json import loads,dumps
from process import read_proc_info
from logger import log_init
from select import select
from time import sleep,time
from ConnectServer import connect_server
import asyncore
'''
#SERVER_HOST = "192.168.0.147"
SERVER_HOST = "192.168.0.199"
SERVER_POST = 8080
'''
config = {}
count = 0

##################################################################
def client_select(sock):
    sock_lock = threading.Lock()        # 创建线程锁，防止sock被关闭

    def read_thread():
        while True:
            rs, _, _ = select([sock], [], [], 10)
            for r in rs:
                sock_lock.acquire()     # 申请线程锁
                if not sock:
                    sock_lock.release() 
                data = sock.recv(1024)
                sock_lock.release()

                print("获取的数据：", data)
    
    def send_data(data):
        serialized_data = dumps(data)       # 序列化数据，转换成JSON格式
        sock.sendall(bytes(serialized_data,"utf-8"))

    def send_tasks():
        timing = float(config["send_interval"])
        t = threading.Timer(timing,read_proc_info_task)
        t.start()

    def read_proc_info_task():
        global count
        print(read_proc_info())
        send_data(read_proc_info())     # 发送进程数据
        send_data(count)
        count += 1
        send_tasks()                     # 定期发送

    read_thread = threading.Thread(target=read_thread)
    read_thread.setDaemon(True)     #守护线程
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
    log_init()
    config = read_config()
    sock = connect_server(config["host"], int(config["port"]), 5)
    
    print(sock)
    client_select(sock)
    #Regular_tasks()
    while True:
        print("主线程正在运行...")
        sleep(20)