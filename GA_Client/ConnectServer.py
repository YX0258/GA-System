import socket
from time import sleep

def connect_server(server_ip, server_port, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while count:
        try:
            sock.connect((server_ip, server_port))
        except (ConnectionRefusedError,TimeoutError) as conn_refuse:
            print(conn_refuse)
        else:
            print("连接成功。")
            break
        count -= 1
        sleep(1)
        print("连接失败，尝试重连...")

    return sock
