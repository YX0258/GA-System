# coding: utf-8

# https://pymotw.com/2/select/
import select
import socket
import queue
from json import loads,dumps
from time import sleep
from readconfig import read_config 
'''
HOST    = "192.168.0.199"
#HOST    = 'localhost'
PORT    = 8080      #服务器端口号
LISTEN  = 5         #监听数量,同时处理的数量
'''

config_list = {
    "HOST": None,
    "PORT": None
}

def dbg(*args):
    print(*args)
    #pass

DisConnect_flag = False     #断开连接标志

def server_init(host, port, listen):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
    server.setblocking(False)   # 非阻塞
    print(host)
    print(port)
    server.bind((host,int(port)))    # 绑定地址
    server.listen(listen)       # 开始监听并设置最大连接数
    server.listen()
    return server               

def server_select(server):
    read_list  = [server]       # 监听列表存放准备 读取 的客户端套接字，服务器也是客户端
    write_list = []             # 存放准备 写入 的客户端套接字
    time_out   = 0              # select() 超时时间 
    message_queues = {}         # 消息队列，存放待处理数据


    def del_sock(sock):
        if sock in write_list:
            write_list.remove(sock)     # 从 write_list 中移除
        read_list.remove(sock)          # 从 read_list  中移除
        sock.close()                    # 关闭套接字
        if not writable:                # 没有待处理的数据
            del message_queues[sock]    # 从消息队列移除

    def get_all_client_ip():
        clients_ip = []
        for sock in read_list:
            clients_ip.append(sock)
        dbg("已连接的客户端：", clients_ip[1:])

    while read_list:    # 监听 read_list 中的服务器和客户端
        
        # 当调用socket的send, recv函数，将会再次调用此模块
        readable, writable, exceptional = select.select(read_list, write_list, read_list, time_out)
        #dbg("事件：",len(readable), len(writable), len(exceptional))
        
        # 循环判断是否有客户端连接进来, 当有客户端连接或断开时select 将触发
        for sock in readable:  
            if sock is server:                      # 是服务端触发，说明有新客户端连接进来
                client, client_address = sock.accept()
                dbg ('connection from', client_address)
                client.setblocking(0)                   # 非阻塞
                read_list.append(client)                # 将新客户端加入监听列表
                message_queues[client] = queue.Queue()  # 单独创建消息队列，保存客户端发来的消息
                get_all_client_ip()
            else:                                   # 是客户端（老用户）触发，处理客户端发来的数据
                try:
                    data = sock.recv(1024)              # 读取数据
                    if data == b'':                     # 客户端主动断开连接
                        dbg ('closing', client_address)
                        del_sock(sock)
                    else:                               # 客户端未断开，处理客户端发来的消息
                        dbg ('received "%s" from %s' % (data, sock.getpeername()))
                        message_queues[sock].put(data)  # 数据放进对应客户端的消息队列中
                        if sock not in write_list:
                            write_list.append(sock)                
                except:
                    dbg(sock.getpeername(),"客户端出现异常，已断开连接")
                    del_sock(sock)

        # 无新客户端连接, 无客户端发送消息时, 开始处理消息队列、保存客户端发来的消息
        for sock in writable:
            dbg("准备处理数据...")
            try:
                message_queue = message_queues.get(sock)
                got_data = message_queue.get_nowait()
                if sock not in read_list:               # 客户端已断开连接(数据还没处理就断开连接)
                    del message_queues[sock]            # 从消息队列移除                
            except queue.Empty:
                dbg("消息队列数据为空")  # 若中途客户端连接，出现错误，注释掉
                if sock in write_list:
                    write_list.remove(sock)
            else:       # 消息队列不为空
                #####################################
                print("数据长度：", len(got_data))
                dbg("未序列化：", got_data)
                try:
                    deserialized_data = loads(got_data)   # 序列化数据，将JSON格式转化为字典格式
                    dbg("已序列化：", deserialized_data)
                except:
                    print("数据太多了，序列化失败....")
                #####################################

        # 处理异常的情况
        for sock in exceptional:
            dbg ('exception condition on', sock.getpeername())
            # Stop listening for input on the connection
            read_list.remove(sock)
            if sock in write_list:
                write_list.remove(sock)
            sock.close()
            del message_queues[sock]

        #sleep(1)

# The script starts here
if __name__ == "__main__":
    config = read_config()
    server_select(server_init(config["host"], config["port"], 5))
    