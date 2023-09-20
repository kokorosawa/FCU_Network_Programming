from mysocket import Mysocket

if __name__ == '__main__':
    s = Mysocket(6666)
    msg = s.listenPort()
    print(msg)
	