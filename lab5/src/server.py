from Server_class import Mysocket
import sys
import threading

def server_task(port):
    main_thread = Mysocket(int(port))
    main_thread.listenPort()
    i = 1
    while True:
        t_name = 'Thread ' + str(i)
        i += 1
        #print('Number of threads: %d\n' % threading.active_count())
        #print('Waiting to receive message from client\n')
        client, (rip, rport) = main_thread.socketAccept()
        #print('Got connection. Create thread: %s\n' % t_name)
        t = Mysocket(thread_name = t_name, client = client, serverIP = rip, PORT = rport)
        t.start()

if __name__ == '__main__':
    server_task(6666)