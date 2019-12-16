import CarConnection
import CarEngine

CARID='CAR01'

host = "127.0.0.1"
port = 61116

def msghandler(msg):
    print('handler msg %s'%msg)
    if msg.startswith('ABCABC'):#动作包
        a = int(msg[6:8])
        if a == 0:
            print('停止')
            # engine.stop()
        elif a == 1:
            print('左转')
            # engine.turnleft()
        elif a == 2:
            print('后退')
            # engine.backward()
        elif a == 3:
            print('右转')
            # engine.turnright()
        elif a == 5:
            print('前进')
            # engine.forward()
    pass

if __name__ == "__main__":
    carconn = CarConnection.CarConnection(host,port,msghandler)
    carconn.conn()
    engine = CarEngine.MyEngine()