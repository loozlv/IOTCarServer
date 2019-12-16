'''********************************************************
    Func Name:    addZero
    Para:         x    :  字符串
                  y    :  长度
    return:       x    :  处理后的字符串
    Desc:         将字符串修改为指定长度，不足的补0，只限于加长，不剪短
    Date:         20190711
    Auth:         yanerfree
********************************************************'''
def addZero(x, y):
    while True:
        if len(x) < y:
            x = '0' + x
        else:
            break

    return x
'''********************************************************
    Func Name:    hexToInt
    Para:         h:16进制数
    return:       datalen:  10进制数
    Desc:         #将 16进制数 转换为  INT
    Date:         20190711
    Auth:         yanerfree
********************************************************'''
def hexToInt(h):
    return int(h,16)

'''********************************************************
    Func Name:    intToHex
    Para:         n    :  10进制数
                  x    :  几个字节
    return:       16进制字符串
    Desc:         将 16进制数 转换成对应的16进制字符串，并根据字节长度补0，不带0x或者 x
    Date:         20190711
    Auth:         yanerfree
********************************************************'''
def intToHex(n, x):
    num = hex(n)
    #print(num)
    num_list = num.split('0x')[1:]#num_list = num.split('0x')[1]

    return addZero(num_list[0].upper(), x*2)

'''********************************************************
    Func Name:    checkValue
    Para:         h  :  需要做异或的16进制字符串
    return:       value : 异或结果
    Desc:         将传入的16进制按2位(8bit) 做异或运算，前2个异或后的结果与下一个异或，一直到结束
    Date:         20190712
    Auth:         yanerfree
********************************************************'''
#将2位的16进制转换成能够用户异或计算的16位数，即'6F'--> 0x6F  --> 10进制
#16进制转10进制
def add0x(s):
    return eval('0x'+s)

def checkValue(h):
    #先取前2组，每组2个做异或运算
    value = add0x(h[0:2]) ^ add0x(h[2:4])#异或后是10进制数

    for i in range(4, len(h), 2):
        value = value ^ add0x(h[i:i+2])
        #print('异或结果--10进制：',value)
        #print('异或结果--16进制：',hex(value))
        #print('转换成16进制intToHex(value, 1):',intToHex(value, 1))
        #value = add0x(intToHex(value, 1))

    value = intToHex(value, 1)#16进制的校验值，1个字节
    return value.upper()


import hashlib
import random
import time
import requests
import json


def byte2hex(bins):
    """ Convert a byte string to it's hex string representation e.g. for output. """
    return ''.join( [ "%02X" % x for x in bins ] ).upper().strip()


def hx2byte(hexstr):
    """ Convert a string hex byte values into a byte string. The Hex Byte values may or may not be space separated. """
    return bytes.fromhex(hexstr)

def crc16(strbuf, lenth):
    result = 0
    tempcrc16 = 0
    tempdata = 0
    m = 0
    n = 0
    result = result
    for m in range(lenth):
        result = (result & 0xFFFF)  # 因为Python的int整形数没有最大值，所以需要&上0xffff
        tempcrc16 = (tempcrc16 & 0xFFFF)  # 因为Python的int整形数没有最大值，所以需要&上0xffff
        tempdata = (tempdata & 0xFFFF)  # 因为Python的int整形数没有最大值，所以需要&上0xffff
        tempcrc16 = (((result >> 8) ^ strbuf[m]) & 0xffff)
        tempdata = (tempcrc16 << 8)
        tempcrc16 = 0
        for n in range(8):
            if (tempdata ^ tempcrc16) & 0x8000:
                tempcrc16 = (((tempcrc16 << 1)) ^ 0x1021)
            else:
                tempcrc16 = (tempcrc16 << 1)
            tempdata = (tempdata << 1)
                # print(tempcrc16)
        result = ((result << 8) ^ tempcrc16)
    return result


def getSig(token='sparktest'):
    rand = str(random.randint(10000, 999999))
    timestamp = str('%.0f'%time.time())
    a = []
    a.append(token)
    a.append(timestamp)
    a.append(rand)
    a.sort()
    sig = hashlib.sha1(''.join(a).encode()).hexdigest()
    return rand,timestamp,sig


def sendData(url,data,file=None):
    rand, timestamp, sig = getSig()
    keystr = str(random.randint(10000, 999999))

    data['ranum']=rand;
    data['timestamp'] =timestamp;
    data['signature'] =sig;
    data['keystr'] = keystr;

    reTry = 0
    while True:
        print('send to url>>%s'%url)
        print("send data>>%s"%data)
        rsp = requests.post(url, data=data,files=file);
        rspcode = rsp.status_code;
        content = rsp.content.decode().strip();
        print("code[%d],content[%s]"%(rspcode,content))
        if rspcode == 200 :
            jsContent=json.loads(content)
            returnCode=jsContent['returnCode']
            returnMsg=jsContent['returnMsg']
            if returnCode == '000000':
                return True, jsContent
            else:
                print('returnCode:%s'%returnCode)
                print('returnMsg:%s'%returnMsg)
                return False;
        else:
            reTry += 1;
        if reTry >= 3:
            return False;


def txt2hex(txt):
    rst = ''
    for c in txt:
        rst += intToHex(ord(c),1)
    return rst


def hex2txt(hexstr):
    cs = ''
    idx = 0
    while idx < len(hexstr):
        cs += chr(int(hexstr[idx:idx+2],16))
        idx += 2
    return cs