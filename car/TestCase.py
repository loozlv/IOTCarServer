# import CarEngine

running = True

# engine = CarEngine.MyEngine()

while running:
    a = input("请输入一个整数:\n0:停止 \n2:后退 \n1:左转 \n3:右转 \n5:前进 \n8:退出\n")
    a = int(a)
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
    elif a == 8:
        print('退出')
        # engine.stop()
        running = False
        break

# engine.release()