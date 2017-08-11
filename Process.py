#coding=utf-8
import threading
import socket

class Process(object):
    def __init__(self,address,addresses):
        #u ip表示进程所在的位置
        self.address = address
        #获取所有进程所在位置
        self.addresses = addresses
        #启动一个监听线程，时刻监听指定端口是否有数据传来
        p = threading.Thread(target=self.waitData(), args=())
        p.start()
        p.join()


    def waitData(self):
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(self.address)
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
                        for i in range(0,len(self.addresses)):
                            if self.addresses[i] != self.address:
                                self.broadCast(self.addresses[i], data)
                        '''
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
                        '''
                    # 此处为相关处理的代码
                    self.doSomething()
                    # 此处为存入数据库过程
                    self.loadToDB(data)

        server.close()

    #广播数据给其它进程
    #dailynum表示流水号
    #hashval表示哈希值
    #cost表示费用
    def broadCast(self,address,data):
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
    #七个进程的位置
    address1 = (ips[0], ports[0])
    address2 = (ips[0], ports[1])
    address3 = (ips[0], ports[2])
    address4 = (ips[1], ports[0])
    address5 = (ips[1], ports[1])
    address6 = (ips[1], ports[2])
    address7 = (ips[1], ports[3])
    addresses = [address1,address2,address3,address4,address5,address6,address7]

    p1 = Process(address1,addresses)