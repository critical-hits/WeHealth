import socket

#给指定ip主机的进程发送数据
def sendData(data,ip,port=8000):
    address = ('10.39.167.101', 8001)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send('jianghezhi,client')
    client.close()
