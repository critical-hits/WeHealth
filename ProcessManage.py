import socket
import threading

class ProcessManage(object):
    def __init__(self,addresses):
        t = threading.Timer(30, self.sync(addresses))
        t.start()

    def sync(self,addresses):
        data = 'synchronized#sync'
        client = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        for i in range(0,len(addresses)):
            client.connect(addresses[i])
            client.send(data)
            client.close()

if __name__=="__main__":
    '''
        ips = ['192.168.43.235', '192.168.43.113', 'localhost']
        ports = [8001, 8002, 8003]
        # 七个进程的位置
        address1 = (ips[0], ports[0])
        address2 = (ips[0], ports[1])
        address3 = (ips[1], ports[0])
        address4 = (ips[1], ports[1])
        address5 = (ips[2], ports[0])
        address6 = (ips[2], ports[1])
        address7 = (ips[2], ports[2])
        '''
    ips = ['192.168.43.113', 'localhost']
    ports = [8001, 8002, 8003, 8004]
    # 七个进程的位置
    address1 = (ips[0], ports[0])
    address2 = (ips[0], ports[1])
    address3 = (ips[0], ports[2])
    address4 = (ips[1], ports[0])
    address5 = (ips[1], ports[1])
    address6 = (ips[1], ports[2])
    address7 = (ips[1], ports[3])
    addresses = [address1, address2, address3, address4, address5, address6, address7]
    pm = ProcessManage(addresses)