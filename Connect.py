import socket

#给指定ip主机的进程发送数据
def sendData(data,ip,port=8000):
    address = (ip, port)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send(data)
    data = client.recv(1024)
    print data
    client.close()

#各个进程都时刻监控自身指定的端口，一旦有数据过来，立马接收
def recData(ip,port=8000):
    #ip为该进程所在主机的ip地址，默认prot=8000
    address = (ip, port)
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(7)

    while True:
        conn, addr = server.accept()
        while True:
            data = conn.recv(1024)
            print data
            # conn.sendall(data)
            if not data:
                conn.close()
                break
    server.close()