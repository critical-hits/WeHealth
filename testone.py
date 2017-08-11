import socket

if __name__ == '__main__':
    address = ('127.0.0.1', 8000)
    client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    client.connect(address)
    client.send('hello-world')
    data = client.recv(1024)
    print data
    client.close()