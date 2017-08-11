import threading
import socket
import numpy

class Process(object):
    def __init__(self, ip,rec_port):
        #ip表示进程所在的自身ip
        self.ip = ip
        #rec_port表示该进程的端口号
        self.port = rec_port
        #启动一个监听线程，时刻监听指定端口是否有数据传来
        p = threading.Thread(target=self.waitData(), args=())
        p.start();
        p.join();

    #获取所有ip地址
    def setIps(self,ips):
        self.ips = ips

    #获取所有端口号
    def setPorts(self,ports):
        self.ports = ports

    def waitData(self):
        # ip为该进程所在主机的ip地址，port为该进程接收数据的端口
        address = (self.ip, self.port)
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(7)
        while True:
            conn, addr = server.accept()
            while True:
                data = conn.recv(1024)
                #接收到数据之后，首先广播到其它各个节点中去，然后进行相关的处理
                #此处为广播到其它节点的代码
                for i in range(0,len(self.ips)):
                    for j in range(0,len(self.ports)):
                        if self.ports[j] != self.port:
                            self.broadCast(self.ips[i],self.ports[j],data)
                # 此处为相关处理的代码
                self.doSomething()
                #此处为存入数据库过程
                self.loadToDB(data)

        server.close()

    #广播数据给其它各进程
    #dailynum表示流水号
    #hashval表示哈希值
    #cost表示费用
    def broadCast(ip,port,data):
        address = (ip, port)
        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        client.connect(address)
        client.send(data)
        data = client.recv(1024)
        print data
        client.close()

    def doSomething(self):
        print ""

    def loadToDB(self,data):
        print ""