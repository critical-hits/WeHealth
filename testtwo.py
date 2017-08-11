import socket

if __name__ == '__main__':
    address = ('127.0.0.1', 8000)

    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(address)
    server.listen(7)

    while True:
        conn, addr = server.accept()
        while True:
            data = conn.recv(1024)
            print data
            #conn.sendall(data)
            if not data:
                conn.close()
                break
    server.close()