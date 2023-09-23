from mysocket import Mysocket
import time

if __name__ == '__main__':
    c = Mysocket(6666)
    msg = int(input("input number:"))
    # msg = 7
    c.connect()
    # c.send(0)
    # c.clientReceive()
    while True:
        c.send(msg)
        msg = c.clientReceive() - 1
        
        if msg <= 0:
            c.stop()
            break
        print(msg)
    