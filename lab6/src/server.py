from mysocket import Mysocket

def server_task(port):
    s = Mysocket(int(port))
    s.listenPort()
    
if __name__ == '__main__':
    server_task(6666)