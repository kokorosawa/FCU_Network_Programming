from mysocket import Mysocket
import time

if __name__ == '__main__':
    c = Mysocket(6666)
    msg = 7
    c.connect()
    while msg != 0:
        c.send(msg)
        msg = c.clientReceive()
    