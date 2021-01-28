import socket
from time import sleep

def connect_server(server_ip, server_port, count):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while count:
        try:
            #sock.bind(("192.168.0.200", 64296))     #设置客户端IP
            sock.connect((server_ip, server_port))
        #except (ConnectionRefusedError,TimeoutError) as conn_refuse:
        except socket.error:
            #print(conn_refuse)
            print("连接失败！请检查服务器是否开启或服务器IP是否正确。")
            print(socket.error)
        else:
            print("连接成功。")
            break
        count -= 1
        sleep(1)
        print("正在尝试重连...")

    return sock
