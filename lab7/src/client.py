from mysocket import Mysocket
import time
import sys


def client_task(msg, port):
    c = Mysocket(int(port), serverIP="127.0.0.1")
    msg = int(msg)
    while True:
        c.send(msg)

        if msg == 0:
            break
        msg = c.clientReceive() - 1

        if msg < 0:
            break
    c.ssl_conn.close()


if __name__ == "__main__":
    msg = int(input("input number:"))
    client_task(msg, 6666)
