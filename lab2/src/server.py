from mysocket import Mysocket

if __name__ == '__main__':
    s = Mysocket(6666)
    s.listenPort()
    msg = s.serverReceive()
    # msg = s.listenPort()
    # while 1:
    #     s.sendmsg(msg)
    #     msg = s.listenPort()
    #     s.reopenPort()
    #     print(msg)
        
        
        
	