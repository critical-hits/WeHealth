# -*- coding: utf-8 -*-

#数据库操作
import sqlite3
import os

'''
常量
'''
#表名称
TABLE_NAME = ''

'''
数据库操作类
'''
class databaseClass:

    def __init__(self):

        global TABLE_NAME
        TABLE_NAME = 'block'

        self.conn = sqlite3.connect("wehealth.db")
        self.cursor = self.conn.cursor()

        #如果存在数据表，则删除
        drop_table_sql = 'drop table if exists ' + TABLE_NAME
        self.cursor.execute(drop_table_sql)

        #创建数据库表block
        create_table_sql = "create table %s " \
              "(id varchar(20) primary key, " \
              "money int(10), " \
              "description varchar(20), " \
              "hashValue varchar(500))" % (TABLE_NAME)
        self.cursor.execute(create_table_sql)

        #插入初始数据
        self.insertOp('0', 0, '', '', )

    # 插入数据
    def insertOp(self, n_id, n_money, n_descrip, n_hash):
        insertStr = "insert into block (id, money, description, hashValue) " \
                    "values ( %s, %d, '%s', '%s')" \
                    % (n_id, n_money, n_descrip, n_hash)
        self.cursor.execute(insertStr)

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

    def closeConn(self):
        self.cursor.close()
        self.conn.commit()
        self.conn.close()

'''
db = database()

db.insertOp('1', 100, "test", '00283744537')
db.insertOp('2', 23, 'second', '00477278767')
db.insertOp('3', 34, 'last', '00283598439')
db.insertOp('5', -20, 'down', '00787592758')
db.insertOp('8', -35, 'last', '00283594339')


print db.selectOp('1')

print db.selectOpDes('last')

print db.selectAll()

print db.calMoney()

db.clearTable()
print db.selectAll()

db.closeConn()
'''