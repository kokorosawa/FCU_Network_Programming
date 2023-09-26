from mysocket import Mysocket
import time
import sys


def client_task():
    c = Mysocket(int(sys.argv[1]))
    # msg = int(input("input number:"))
    msg = 7
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

if __name__ == '__main__':
    client_task()
    
    