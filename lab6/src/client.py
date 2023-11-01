from mysocket import Mysocket

def resend(port,msg):
    c = Mysocket(int(port))
    msg = int(msg)
    c.send(msg)
    c.Socket.settimeout(0.01)
    return c

def client_task(port,msg):
    try:
        c = resend(port,msg)
        while msg > 0:
            msg = c.clientRecv()
            c.send(msg)
        c.Socket.close()
    except Exception as e:
        c = resend(port,msg)
    print('[Client]:Close the socket')

if __name__ == '__main__':
    client_task(6666, 10)