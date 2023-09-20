from mysocket import Mysocket
import time

if __name__ == '__main__':
    c = Mysocket(6666)
    c.connect()
    c.send(7)
    c.clientReceive()
    c.send(6)
    # while msg != 0:
    #     c.sendmsg(msg)
    #     msg -= 1
    