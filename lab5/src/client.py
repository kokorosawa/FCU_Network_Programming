from Client_class import Mysocket
import time
import sys


def client_task(msg,port):
    msg = int(msg)
    while msg > 0:     
        c = Mysocket(int(port))
        msg = int(msg)
        c.connect()
        c.send(msg)
        msg = int(c.clientReceive() - 1)
        
        if msg <= 0:
            c.stop()
            break

if __name__ == '__main__':
    msg = int(input("input number:"))
    client_task(msg,6666)
    