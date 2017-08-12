#coding=utf-8

import connection
from BlockChain import BlockChain
from database import database
import collections
from operator import itemgetter
from Block import Block
#import DB.py


class Accounting(object):
    def __init__(self,chain=None,hashChain=None):
        self.chain= chain
       # self.hashChain=hashChain

    def seek_lastHash(self):
        #数据库操作调出最新的hash，比对其他人的
        # s= str(sql)
        if self.chain.head!=None:
            #return self.chain.head.previous_hash
            return self.chain.head.hash()
        else:
            r= database.dbcon.get_lasthash()
            hash=Block(r[0][0],r[0][1],r[0][2],r[0][3]).hash()
            #return database.dbcon.get_lasthash()
            return hash
        return
    '''
    def synchro_database(self,bc):
        ''''''同步数据库
        bc数据库 写入区块链
        for c in 数据库
            bc.add_block(c)
        ''''''
        return

    def synchro_blockchain(self,bc):
        # 同步其他节点的账目
        #
        return
        #对账

        #请求账目
    '''

    # 判断当前的账目是否一致
    #sychroTable 传入的hash对账表 字典格式{ip：hash}
    #chash 当前的hash值
    #retun 如果链正确，返回空否则 返回正确账本的ip地址
    def get_correctAccount(self,sychroTable,chash):
        #初始化账本
        if self.chain:
            hc = self.chain.blockchain
        else:
            bc=BlockChain()
            bc.synchro_fromDatabase()#如果关机重启了，从数据库同步账本
            hc=bc.blockchain

        #统计认可度最高的hash
        t=collections.Counter(sychroTable.values())
        a=sorted(collections.Counter(sychroTable.values()))
        b=0
        righthash=0
        for i in t.keys():
            if t[i]>b:
                b=t[i]
                righthash=i
        #righthash=max(t.values())

        #Sfor m in
        for k in sychroTable.keys():
            if sychroTable[k]==righthash:
                ipaddress=k
                break;

        #查自身的链表
        if righthash!=chash:
            return {righthash: ipaddress}
        for i in range(1,len(hc)):
            print hc[i-1].hash()
            print hc[i].get_previoushash()
            if hc[i-1].hash()!=hc[i].get_previoushash():
                return {righthash: ipaddress}
        return None
        #

    #发送对账请求
    def request_synchro(self,hash):
        #send hash
        message='1;'+id+';'+hash
        connection.sendBroadcast(message)

    #发送账本同步请求
    def requst_account(self,id,ipaddress):
        #发送账目接收请求
        message='3'
        connection.sendtoPoint(message,ipaddress)

    #接收到账本后调用来同步账本，写入数据库
    def get_accountbook(self,bChain,accountbook):
        bChain.dbsql.clearTable()
        jj=bChain.get_fromJson(accountbook)
        bChain.save_allChain(jj)
        return
        '''
        接收账本,直接入库
        stringLine = str.split(accountbook,'|')
        for i in range(0,len(stringLine)):
            dataBlock = str.split(stringLine[i],',')
            b = Block(dataBlock[0],dataBlock[1],dataBlock[2],dataBlock[3])
            self.save_blockchain(b)
        '''#


