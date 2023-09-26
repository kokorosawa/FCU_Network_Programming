from mysocket import Mysocket
import sys

def server_task(port):
    s = Mysocket(int(port))
    s.listenPort()
    msg = s.serverReceive()

if __name__ == '__main__':
    server_task(6666)