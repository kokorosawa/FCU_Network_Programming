from mysocket import Mysocket
import sys

def server_task():
    s = Mysocket()
    s.listenPort()
    msg = s.serverReceive()

if __name__ == '__main__':
    server_task()