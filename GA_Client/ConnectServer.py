import socket
from time import sleep



def connect_server(server_ip, port, count):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while count:
        try:
            sock.connect((server_ip, port))
        except ConnectionRefusedError as conn_refuse:
            print(conn_refuse)
        else:
            print("连接成功。")
            sock.sendall(bytes("666", "utf-8"))
            break
        count -= 1
        sleep(1)

    return sock

'''
print("test")
connect_server("192.168.0.147", 8080, 5)
'''