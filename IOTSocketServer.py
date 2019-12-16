# coding:utf-8

import socketserver
import Utils
import socket
import threading
import Utils

#传输数据格式
# str -- > bytes ---> HexStr ---> 封装报文体 （body = head+len(hexstr)+hexstr）--->sendall(bytes(body,'utf-8))

DEPART_STR='FAFBFC'
DEPART_STR_LEN=len(DEPART_STR)
KEEPALIVE='FDFDFD44544C44FDFDFD'

#已登录的客户端 session列表
sessions = []

#协议
#注册包
# AABBCC000c6D6F62303032
# AABBCC010c6D6F62303032
#AABBCC+00/01+len(1)+name
#00 car
#01 mobile
TYPE_CAR = '00'
TYPE_MOBILE = '01'

# 获取对端设备列表
# mytyp 自己设备类型
def formatTYP(mytyp):
    tmp = []
    others = []
    for sess in sessions:
        print(sess)
        if sess.devType != mytyp and sess.devName is not None:
            tmp.append(sess.devName)
            others.append(sess)

    rst = Utils.intToHex(len(tmp),1)
    for t in tmp:
        namelen = len(t)
        rst += Utils.intToHex(namelen,1)
        rst += t
    return rst,others


def findCarByName(carname):
    for sess in sessions:
        if sess.devName == carname:
            return sess
    return None


class IotSession:

    def __init__(self, _threadname, _instance, _addr, _devType = None, _devName = None):
        self.threadname = _threadname;
        self.instance = _instance
        self.addr = _addr
        self.devType = _devType
        self.devName = _devName

    def __str__(self):
        tname = ''
        if self.devName is not None:
            tname = Utils.hex2txt(self.devName)
        return "%s,%s,%s,%s"%(self.devType,tname,self.threadname,self.addr)


def delsessionbythreadname(_threaname):
    for sess in sessions:
        if sess.threadname == _threaname:
            sessions.remove(sess)


def updatedevtype(_threaname,_devtype,_devname):
    for sess in sessions:
        if sess.threadname == _threaname:
            sess.devType = _devtype
            sess.devName = _devname


class MyServer(socketserver.BaseRequestHandler):  # 类继承socketserver.BaseRequestHandler

    def paserHex(self,hexData):
        if KEEPALIVE in hexData:
            print('KeepAlive...')
            hexData=hexData.replace(KEEPALIVE,'')
            if len(hexData) > 0:
                print('have more>>'+hexData)
                self.paserHex(hexData)
        elif hexData.startswith('AABBCC'):#注册包
            clienttype = hexData[6:8]
            clientnamelen = hexData[8:10]
            clientname = str(hexData[10:10+int(clientnamelen,16)])
            updatedevtype(threading.currentThread().getName(), clienttype, clientname)
            if clienttype == TYPE_MOBILE:
                msg,others = formatTYP(clienttype)
                self.request.sendall(bytes(msg,'utf-8'))

                for other in others:
                    other.instance.request.sendall(bytes('hello','utf-8'))
        elif hexData.startswith('ABCABC'):#透传包
            clientnamelen = int(hexData[6:8], 16)
            clientname = str(hexData[8:8+clientnamelen])
            actionId= hexData[8+clientnamelen:8+clientnamelen+2]
            carsession = findCarByName(clientname)
            if carsession is not None:
                carsession.instance.request.sendall(bytes('ABCABC'+actionId,'utf-8'))
            else:
                self.request.sendall(bytes('00', 'utf-8'))
            pass
        else:
            print("not implemented")
            return
        pass

    def setup(self):
        connid = threading.currentThread().getName()
        sess = IotSession(connid, self, self.client_address)
        print(sess.addr, "is connected")
        sessions.append(sess)
        pass

    def finish(self):
        print(self.client_address,"is finish")
        connid = threading.currentThread().getName()
        delsessionbythreadname(connid)
        print(len(sessions), sessions)
        pass



    def handle(self):
        # self.request.sendall(bytes('欢迎使用DTLD服务。',encoding='GBK'))
        while True:
            try:
                data = self.request.recv(1024)
                if len(data) == 0:
                    print("empty data skip")
                    break
                hexData = Utils.byte2hex(data)
                print("[%s] says:%s" % (self.client_address, hexData))
                # print("Hex>>%s" % hexData)
                self.paserHex(hexData)
                # self.finish()
            except Exception as e:
                print("Exception :", e)
                return;


def start():
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 61116), MyServer)
    server.allow_reuse_address = True

    try:
        server.serve_forever()
    except Exception as e:
        print(e)

    server.server_close();
    print("=======================")

print(__name__)

if __name__ == '__main__':
    start()

