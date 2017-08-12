#coding:utf-8
import Block
import BlockChain

#global bufer


class BlockBuffer(object):
    def __init__(self):
        self.buffer = {}

    def reciveBlock(self,obj):  # 交易接收函数，存入缓存
        # 数据重复性校验for()  根据发送方的地址判断是否转发不会重复，
        '''
        for key in buffer.keys():
            if (key == obj.id):
                return
        '''
        buffer[obj.identifier] = obj

    def saveBuffer(self,obj): #保存块函数，调用modules的函数实现，把缓存中的块写入数据库周期性调用
        for key in sorted(buffer.keys()):
            buffer[key].setPreHash(obj.getHead().previous_hash if obj.getHead() else None) # 保存前一个区块的hash（）是否改成ID
            obj.add_block(buffer[key])
            obj.insert_database(buffer[key])
            #block.save() 调用dao层
        buffer.clear()
        return

    def sortBuffer(self,obj): # 块排序函数修正缓存块中交易数据顺序，建议调用(3s一次)
        sorted(int(buffer.keys()))

    def cleanBuffer(self,obj):  # 清空缓存块
        buffer.clear()
