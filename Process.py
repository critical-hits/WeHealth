#coding=utf-8
import threading
import socket
from Block import Block
from BlockChain import BlockChain
from BlockBuffer import BlockBuffer
from Accounting import Accounting
from database import database
from time import sleep
from ProcessManage import  ProcessManage
from databaseClass import databaseClass

import json

class Process(object):
    def __init__(self,address,addresses):
        #u ip表示进程所在的位置
        self.address = address
        #获取所有进程所在位置
        self.addresses = addresses
        #创建缓冲区
        self.blockBuffer = BlockBuffer()
        #创建一个字典
        self.directory = {}
        #同步进程
        self.processManage = ProcessManage(self.address,self.addresses)

        self.chain=BlockChain()

       # t1=threading.Thread(target=self.watch(), args=())
       # t1.start()
       # t1.setb
        #t1.setDaemon(True)

        #启动一个监听线程，时刻监听指定端口是否有数据传来
        p = threading.Thread(target=self.waitData, args=())
        p.start()
        #p.join()

        #周期性调用，每隔3秒对缓冲区内的块进行排序
        # t1 = threading.Timer(3, self.blockBuffer.sortBufer())
        # t1.start()
        # t1.join()


       # t1 = threading.Thread(target=self.watch, args=())
       # t1.start()

        #t1 = threading.Timer(3, self.watch())
        #t1.start()
        #t1.join()


        #周期性调用，每隔5秒将缓冲区的块数据写入数据库和本地链条
        self.writData()
        #t2 = threading.Timer(5, self.writData)
        #t2.start()
        #t2.join()

        #每隔一定时间通知进程执行同步操作
        sleep(10)
        self.processManage.sync()

    def watch(self):
        #print 'asdasf'
        while True:
            r=database.dbcon.selectAll()
            for ii in range(0,len(r)):
                print r[ii]
            sleep(2)

    def writData(self):
            #self.blockBuffer.sortBuffer()
            bc=self.chain
            self.blockBuffer.saveBuffer(bc)
            self.blockBuffer.cleanBuffer()
            t2 = threading.Timer(5, self.writData)
            t2.start()

    #监听线程，时刻监听指定端口是否有数据传来
    def waitData(self):
        server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('',self.address[1]))
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
                    datas = data.split('#')
                    if datas[1] == 'client':
                        # 接收到数据之后，首先广播到其它各个节点中去，然后进行相关的处理
                        # 此处为广播到其它节点的代码
                        for i in range(0,len(self.addresses)):
                            if self.addresses[i] != self.address:
                                self.broadCast(self.addresses[i], data)
                        # 此处将数据放入区块链进行相应处理
                        self.doSomething(datas[0])
                    if datas[1] == 'broadcast':
                        self.doSomething(datas[0])

                    if datas[1] == 'requestBook':
                        self.send_book(datas[0])
                        print '...'
                        #请求账本，要实现发送账本-- fly --
                    if datas[1] == 'sendBook':
                        #收到账本，存到数据库 -- fly --
                        self.save_database(datas[0])
                    #若接收到同步信号，则执行同步操作 -- fly --
                    if datas[1] == 'sync':
                        self.sendHashValue()
                        #发送对账状态  -- fly --

                    #若接收到hash值，则一一进行比对
                    #此时接收的data数据格式为ip:port$hashvalue#hashvalue
                    if datas[1] == 'hashvalue':
                        tmp = datas[0].split('$')
                        self.directory[tmp[0]]=tmp[1]
                        # 当已收到其它进程发送过来的hash值时，执行判断同步过程
                        if (len(self.directory) == 3):
                            self.sync()

                    # 此处为存入数据库过程
                    self.loadToDB(data)

        server.close()

    #广播数据给其它进程
    #dailynum表示流水号
    #hashval表示哈希值
    #cost表示费用
    def broadCast(self,address,data):
        datas = data.split('#')
        tmp = datas[0] + '#broadcast'
        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        client.connect(address)
        client.send(tmp)
        client.close()

    def p2p(self,address,data,flag):
        #datas = data.split('#')
        tmp = data + '#'+flag
        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        client.connect(address)
        client.send(tmp)
        client.close()



    #将接受到的数据添加到区块链中
    def doSomething(self,data):
        print "I'm doing something ..."
        tmp = data.split(':')
        #创建一个新区块
        block = Block(tmp[0],tmp[1],tmp[2])
        #将块放入缓冲区
        self.blockBuffer.reciveBlock(block)

    #执行同步操作 -- fly --
    def sync(self):
        ac = Accounting()
        chash=ac.seek_lastHash()
        ipport=ac.get_correctAccount(self.directory,chash)

        if ipport == None:
            #账本是对的，向前台发送正常状态
            '''
            '''
        else:
            ac.requst_account(ipport)
            #向前台发送账本错误状态
            '''
            '''
        print 'syn...'
    # -- fly --
    def requst_account(self,ipport):
        newAddress=(ipport.split(':')[0],ipport.split(':')[1])
        data=str(self.address)
        flag='requestBook'
        self.p2p(newAddress,data,flag)

    #-- fly --
    def save_database(self,accountbook):
        ac=Accounting()
        bc = self.chain
        ac.get_accountbook(bc,accountbook)
        ##发送修正状态码
        '''
        '''
    #-- fly --
    def send_book(self,ipport):
        newAddress = (ipport.split(':')[0], ipport.split(':')[1])
        bc = self.chain
        data = bc.chain_toJson()
        flag = 'sendBook'
        self.p2p(newAddress, data, flag)

    #向其它各进程发送hash值
    def sendHashValue(self):
        ac=Accounting(self.chain)
        hashValue = ac.seek_lastHash()
        print '1  ' + hashValue
        for i in range(0, len(self.addresses)):
            if self.addresses[i] != self.address:
                client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
                client.connect(self.addresses[i])
                #拼接的数据格式为ip:port$hashvalue#hashvalue
                client.send(self.address[0]+':'+str(self.address[1])+'$'+str(hashValue)+'#hashvalue')
                client.close()

    def loadToDB(self, data):
        print "Load to database ..."

if __name__ == '__main__':
    '''
    ips = ['192.168.43.235', '192.168.43.113', 'localhost']
    ports = [8001, 8002, 8003]
    # 七个进程的位置
    address1 = (ips[0], ports[0])
    address2 = (ips[0], ports[1])
    address3 = (ips[1], ports[0])
    address4 = (ips[1], ports[1])
    address5 = (ips[2], ports[0])
    address6 = (ips[2], ports[1])
    address7 = (ips[2], ports[2])
    '''
    ips = ['192.168.43.113', 'localhost']
    ports = [8001, 8002, 8003]
    # 七个进程的位置
    address1 = (ips[1], ports[0])
    address2 = (ips[1], ports[1])
    address3 = (ips[1], ports[2])
    #address4 = (ips[0], ports[3])
    #addresses = [address1, address2, address3, address4]
    addresses = [address1, address2, address3]
    p = Process(address1, addresses)