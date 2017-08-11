import socket

#给指定ip主机的进程发送数据
def sendData(data,ip,port=8000):
    address = (ip, port)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send(data+',client')
    client.close()
