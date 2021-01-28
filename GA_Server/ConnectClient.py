
# encoding: utf-8
import time
import socketserver
import threading

HOST    = "192.168.0.199"
#HOST    = "loaclhost"
PORT    = 8080
TIMEOUT = 50

client_info = {
    "client_ip"   : None,
    "client_data" : None
}


#继承StreamRequestHandler类，并重写其中的handle方法，该方法是在每个请求到来之后都会调用
class ThreadedTCPRequestHandler(socketserver.StreamRequestHandler):
#    def __init__(self, request, client_addr, server):
#        socketserver.StreamRequestHandler.__init__(self, request, client_addr, server)
        
    def handle(self):
        while True:
            data = str(self.request.recv(1024), 'utf-8')
            #try:
            if len(data)>0:
                #保存从客户端接受到的数据和客户端IP
                client_info["client_data"] = str(self.request.recv(1024), 'utf-8')
                client_info["client_ip"]   = self.client_address

                print("client_data = ", client_info["client_data"])
                print("client_ip = ", client_info["client_ip"])
                #cur_thread = threading.current_thread()
                #data = bytes(client_info["client_data"], "utf-8")
                self.wfile.write(data) #write()方法只能写入bytes类型
            else: #except:
                print("finish")
                self.finish()
                break
class GAServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
    def handle_timeout(self):
        print("%s time..." % time.time())

#实现多请求并发处理，继承socketserver.ThreadingMixIn即可，无需处理。
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server.timeout  = 50
    print("server running...")
    '''
    while True:
        print("test...")
        server.handle_request()
        print("test222...")
    '''
    with server:
        print("test...")
        server.serve_forever() 
        print("test222...")   
