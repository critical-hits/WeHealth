#coding:utf-8

from Block import Block#要不要？
#import DB
import json

from databaseClass import databaseClass



class BlockChain(object):#不存数据的链？

    def __init__(self):
        self.head = None   # 指向最新的一个区块
        #self.blocks = {}   # 包含所有区块的一个字典
        self.blockchain=[]  # 包含所有hash的一个数组
        self.dbsql = databaseClass() #数据库操作类

    '''
        添加区块函数
    '''

    def clean_chain(self):
        self.blockchain=[]

    def add_block(self, new_block):
        previous_hash = self.head.hash() if self.head else None
        new_block.previous_hash = previous_hash
        self.blockchain.append(new_block)
        '''
        self.blocks[new_block.identifier] = {
            'block': new_block,
            #'previous_hash': previous_hash,
            #'previous': self.head,
        }
        '''
        self.head = new_block
        #DB.save()
        self.insert_database(new_block)
        #add to database  insert（）
    def __repr__(self):
        num_existing_blocks = len(self.blockchain)
        return 'Blockchain<{} Blocks, Head: {}>'.format(
            num_existing_blocks,
            self.head.identifier if self.head else None
        )

    def get_Head(self):
        return self.head

    def get_headHash(self):
        return self.hashchain

    def get_blockchain(self):
        self.blockchain

    def synchro_fromDatabase(self):# 从数据库中提取完整的账本。。。
        #get from database
        #search all block
        #self.blocks.clear()
        self.clean_chain()
        r= self.dbsql.selectAll()
        for i in range(0,len(r)):
            print r[i]
            b = Block(r[i][0], r[i][1],r[i][2], r[i][3])
            #b=json.loads(r[i]
            self.add_block(b)
        return self.blockchain


    def chain_toString(self):#账本字符串化
        r = self.dbsql.sqlite.selectAll()
        jsonstr=json.dumps(r)
        '''
        str=[]
        for i in self.blocks.keys():
            strblock=str(self.blocks[i]).
            strblock=str(self.blocks[i].identifier)+'~'+str(self.blocks[i].value)+'~'+str(self.blocks[i].data)+'~'+str(self.blocks[i].prvious_hash)
            str+=strblock+'|'
        return str
        '''



    def chain_toJson(self):
        r = self.dbsql.selectAll()
        jsonstr = json.dumps(r)
        return jsonstr

    def get_fromJson(self,jsonstr):
        jsonlist = json.loads(jsonstr)
        return jsonlist

    def insert_database(self,b):
        self.dbsql.insertOp(b.get_identifier(), b.get_value(), b.get_data, b.get_previoushash())

    def save_allChain(self):
        for i in len(self.blockchain):
            self.dbsql.insertOp(self.blockchain.get_identifier(),self.blockchain.get_value(),self.blockchain.get_data,self.blockchain.get_previoushash())
        #保存block到数据库
        #...
        return