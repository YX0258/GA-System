import socket
import threading
from select import select
from time import sleep
from ConnectServer import connect_server

#SERVER_HOST = "192.168.0.147"
SERVER_HOST = "192.168.0.199"
SERVER_POST = 8080

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
                #data = srecv(1024)     # 读取数据
                data = sock.recv(1024)
                sock_lock.release()

                print("获取的数据：", data)
    
    read_thread = threading.Thread(target=read_thread)
    read_thread.setDaemon(True)     #守护线程
    read_thread.start()

        # 测试不断写数据
    for x in range(10):
        print (x)
        sock.sendall(bytes("hello", "utf-8"))
        sleep(.1)  # 交出CPU时间，否则其他线程只能看着
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
    sock = connect_server(SERVER_HOST, SERVER_POST, 5)
    
    #print(sock)
    client_select(sock)
    while True:
        print("主线程正在运行...")
        sleep(.2)