import socket

def sendData(ip,port,data):
    address = (ip, port)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send(data)
    data = client.recv(1024)
    print data
    client.close()