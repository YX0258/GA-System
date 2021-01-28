import socket
from time import sleep
from threading import Thread,Event
from json import loads,dumps
from process import read_proc_info,find_proc

sock_connected = Event()

def upload_data_task(sock,data):
    while True:
        if sock_connected.is_set():
            data = get_pc_info()
            serialized_data = dumps(data)       # 序列化数据，转换成JSON格式
            try:
                print("数据长度：", len(serialized_data))
                sock.sendall(bytes(serialized_data,"utf-8"))
            except sock.error:
                print("服务器主动断开了连接:", sock.error)
                #logger.logging.error(socket.error)
        else:
            sock_connected.wait()   #等待socket连接

def read_proc_info_task():
    while True:
        if sock_connected.is_set()
    Proc_Info = read_proc_info(proc_list)
    print(Proc_Info)
    send_data(Proc_Info)     # 发送进程数据
    send_data(count)

def get_pc_info():
    Proc_Info = read_proc_info(proc_list)
    return data
    

def create_task_thread():
    print("create success!")