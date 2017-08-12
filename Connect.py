# -*- coding: utf-8 -*-
import socket
#from database import database
import threading
#给指定ip主机的进程发送数据
def sendData(data,ip,port=8001):
    address = (ip, port)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send(data+'#client')
    client.close()

def p():
    print 'ok \n'
    t1 = threading.Timer(2,p)
    t1.start()


if __name__ == '__main__':
    sendData('001:99:jianghezhi','localhost',8001)
    sendData('003:99:jianghezhi', 'localhost', 8001)
    sendData('008:99:jianghezhi', 'localhost', 8001)
    sendData('009:99:jianghezhi', 'localhost', 8002)
    sendData('007:99:jianghezhi', 'localhost', 8002)
   # p()
    # r = database.dbcon.selectAll()
    # print r

