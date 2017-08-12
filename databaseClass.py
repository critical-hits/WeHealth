# -*- coding: utf-8 -*-

#数据库操作
import sqlite3
import os
from datetime import datetime

'''
常量
'''
#表名称
TABLE_NAME = ''

'''
数据库操作类
'''
class database:

    def __init__(self):

        global TABLE_NAME
        TABLE_NAME = 'block'

        self.conn = sqlite3.connect("wehealth.db")
        self.cursor = self.conn.cursor()

        #如果存在数据表，则删除
        drop_table_sql = 'drop table if exists ' + TABLE_NAME
        self.cursor.execute(drop_table_sql)

        #创建数据库表block
        create_table_sql = "create table block " \
              "(id varchar(20) primary key, " \
              "money int(10), " \
              "description varchar(20), " \
              "hashValue varchar(500), time datetime )"
        self.cursor.execute(create_table_sql)

        #插入初始数据
        time = datetime.now()
        self.insertOp('0', 0, '', '', time)

    # 插入数据
    def insertOp(self, n_id, n_money, n_descrip, n_hash, n_time):
        insertStr = "insert into block (id, money, description, hashValue, time) " \
                    "values ( ?, ?, ?, ?, ?)"
        self.cursor.execute(insertStr, (n_id, n_money, n_descrip, n_hash, n_time))


    # 删除数据
    def deleteOp(self, n_id):
        deleteStr = "delete from block where id = " + n_id
        self.cursor.execute(deleteStr)

    # 改变数据
    # sqlite好像只能update已有主键的其他字段值，所以此处不考虑改
    # 需要对顺序进行调整的地方，在block逻辑里，通过缓冲区来做
    # def modifyOp(n_id, n_money, n_descrip):

    # 根据id查询某一条数据
    def selectOp(self, n_id):
        selectStr = "select * from block where id = " + n_id
        print selectStr
        self.cursor.execute(selectStr)
        v = self.cursor.fetchall()
        return v

    # 根据description查询某一条数据
    def selectOpDes(self, n_des):
        selectDesStr = "select * from block where description = '%s'" % (n_des)
        print selectDesStr
        self.cursor.execute(selectDesStr)
        v1 = self.cursor.fetchall()
        return v1

    # 查询总账上所有数据
    def selectAll(self):
        selectAllStr = "select * from block"
        print selectAllStr
        self.cursor.execute(selectAllStr)
        va = self.cursor.fetchall()
        return va

    # 计算总账
    def calMoney(self):
        # 把money取出来
        fetchMoney = "select money from block"
        self.cursor.execute(fetchMoney)
        moneyList = self.cursor.fetchall()
        print moneyList
        num = len(moneyList)
        moneyAll = 0
        for m in moneyList:
            moneyAll += m[0]
        print "money all = "
        return moneyAll

    # 清空数据
    def clearTable(self):
        clearStr = "delete from block"
        self.cursor.execute(clearStr)

    # 数据库取最后一行数据  --fly--
    def get_last(self):
        str = "select * from block order by id desc limit 1"
        self.cursor.execute(str)
        va = self.cursor.fetchall()
        return va

    def closeConn(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()
