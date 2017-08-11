#coding=utf-8
import threading
import socket

class Process(object):
    def __init__(self, ip,rec_port,ips,ports):
        #u ip表示进程所在的自身ip
        self.ip = ip
        #rec_port表示该进程的端口号
        self.port = rec_port
        # 获取所有ip地址
        self.ips = ips
        # 获取所有端口号
        self.ports = ports
        #启动一个监听线程，时刻监听指定端口是否有数据传来
        p = threading.Thread(target=self.waitData(), args=())
        p.start()
        p.join()


    def waitData(self):
        # ip为该进程所在主机的ip地址，port为该进程接收数据的端口
        address = (self.ip, self.port)
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(address)
        server.listen(8)
        while True:
            conn, addr = server.accept()
            while True:
                data = conn.recv(1024)
                if not data:
                    print 'over ...'
                    conn.close()
                    break
                else:
                    print data
                    datas = data.split(',')
                    if datas[1] == 'client':
                        # 接收到数据之后，首先广播到其它各个节点中去，然后进行相关的处理
                        # 此处为广播到其它节点的代码
                        for i in range(0, len(self.ips)):
                            for j in range(0, len(self.ports)):
                                #print "i:" + str(i) + " j:" + str(j)
                                if self.ips[i] == self.ip:
                                    if self.ports[j] != self.port:
                                        # 'ip:'+self.ip+' port:'+ str(self.port)
                                        #print self.ips[i] + ' ' + str(self.ports[j])
                                        self.broadCast(self.ips[i], self.ports[j], data)
                                else:
                                    self.broadCast(self.ips[i], self.ports[j], data)
                    # 此处为相关处理的代码
                    self.doSomething()
                    # 此处为存入数据库过程
                    self.loadToDB(data)

        server.close()

    #广播数据给其它进程
    #dailynum表示流水号
    #hashval表示哈希值
    #cost表示费用
    def broadCast(self,ip,port,data):
        address = (ip, port)
        datas = data.split(',')
        tmp = datas[0] + ',broadcast'
        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        client.connect(address)
        client.send(tmp)
        client.close()

    def doSomething(self):
        print "I'm doing something ..."

    def loadToDB(self, data):
        print "Load to database ..."

if __name__ == '__main__':
    ips = ['10.39.167.101', '10.39.167.102']
    ports = [8001, 8002, 8003, 8004]
    p1 = Process('10.39.167.101', 8001, ips, ports)