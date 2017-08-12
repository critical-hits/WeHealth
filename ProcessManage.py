#coding=utf-8
import socket
import threading

class ProcessManage(object):
    def __init__(self,address,addresses):
        self.address = address
        self.addresses = addresses

    def sync(self):
        print 'Account Book'
        data = 'synchronized#sync'

        for i in range(0,len(self.addresses)):
            if self.addresses[i] != self.address:
                print self.addresses[i]
                client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
                client.connect(self.addresses[i])
                client.send(data)
                client.close()

        t = threading.Timer(15, self.sync)
        t.start()


# if __name__=="__main__":
#     '''
#         ips = ['192.168.43.235', '192.168.43.113', 'localhost']
#         ports = [8001, 8002, 8003]
#         # 七个进程的位置
#         address1 = (ips[0], ports[0])
#         address2 = (ips[0], ports[1])
#         address3 = (ips[1], ports[0])
#         address4 = (ips[1], ports[1])
#         address5 = (ips[2], ports[0])
#         address6 = (ips[2], ports[1])
#         address7 = (ips[2], ports[2])
#         '''
#     ips = ['192.168.43.113', 'localhost']
#     ports = [8001, 8002, 8003, 8004]
#     # 七个进程的位置
#     address1 = (ips[0], ports[0])
#     address2 = (ips[0], ports[1])
#     address3 = (ips[0], ports[2])
#     address4 = (ips[1], ports[0])
#     address5 = (ips[1], ports[1])
#     address6 = (ips[1], ports[2])
#     address7 = (ips[1], ports[3])
#     addresses = [address1, address2, address3, address4, address5, address6, address7]
#     p = ProcessManage(addresses)
#     p.sync()