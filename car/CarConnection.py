import socket
import threading
import Utils
import Car

class CarConnection:

    def __init__(self, _host, _port, _msghandler):
        self.host = _host
        self.port = _port
        self.msghandler = _msghandler
        self.sock = None
        self.isConn = False
        self.recvthread = None
        pass

    def recvmsg(self):
        while self.isConn:
            data = self.sock.recv(1024)
            if len(data) > 0:
                recv_data = str(data, 'utf-8')
                print('recv:', recv_data)
                self.msghandler(recv_data)
        print('recv thread exit')

    def conn(self):
        self.sock = socket.socket()
        try:
            self.sock.connect((self.host, self.port))
        except socket.error as e:
            print("Socket Connect Error:%s" % e)
        print("connect success")
        self.isConn = True
        self.recvthread = threading.Thread(target=self.recvmsg, name="recvMsgThread")
        self.recvthread.start()
        carid = Utils.txt2hex(Car.CARID)
        registMsg='AABBCC'+'00'+Utils.intToHex(len(carid),1)+carid
        print('registMsg>>%s'%registMsg)
        self.sendHexMsg(registMsg)

    def sendByteMsg(self, msg):
        if not self.isConn:
            print("socket not connected,call conn first")
            return
        self.sock.sendall(msg)

    def sendHexMsg(self,msg):
        self.sendByteMsg(Utils.hx2byte(msg))

    def sendStrMsg(self,msg):
        self.sendByteMsg(bytes(msg,'utf-8'))


    def stop(self):
        self.isConn = False
        self.sock.close()