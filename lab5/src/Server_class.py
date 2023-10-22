import sys
import socket
import struct
import binascii
import threading
import time

class Mysocket(threading.Thread):
    def __init__(self, thread_name = 'main_thread', client = None, PORT=6666, BUF_SIZE=1024,serverIP='127.0.0.1',backlog=5):
        super().__init__(name = thread_name)
        self.PORT = PORT
        self.BUF_SIZE = BUF_SIZE
        self.backlog = backlog
        self.serverIP = socket.gethostbyname(serverIP)
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client = client
        self.lock = threading.Lock()
        
    def run(self):
        self.serverReceive()

    def connect(self):
        print('[Client]:Connecting to %s port %s' % (self.serverIP, self.PORT))
        self.Socket.connect((self.serverIP, self.PORT))
        
        
    def send(self,num,control ='#'):
        self.control = control
        record = (num, control.encode('utf-8'))		# must encode a string to bytes
        s = struct.Struct('!' + 'i 5s')							# ! is network order
        self.packed_data = s.pack(*record)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            print('[Client]:Send: %d' % num)
            self.Socket.send(self.packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))
            
    def stop(self):
        num = 0
        self.control = "s"
        record = (num, self.control.encode('utf-8'))		# must encode a string to bytes
        s = struct.Struct('!' + 'i 5s')							# ! is network order
        self.packed_data = s.pack(*record)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            self.Socket.send(self.packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))

    def listenPort(self):
        self.Socket.bind(('', self.PORT)) 
        self.Socket.listen(self.backlog)
        print('[Server]:Starting up server on port: %s' % (self.PORT))
        print('[Server]:Waiting to receive message')
        
    def socketAccept(self):
        client, (rip, rport) = self.Socket.accept()
        return client, (rip, rport)
    def serverReceive(self):
        try:
            self.lock.acquire()
            name = threading.current_thread().name
            self.client_msg = self.client.recv(self.BUF_SIZE)
            client_msg = self.client_msg
            if client_msg:
                s = struct.Struct('!' + 'i 5s')# ! is network order (receive format is network order)
                unpacked_data = s.unpack(client_msg)
                print('[Server]:Receive Integer = %d' %(unpacked_data[0]))
                record = int(unpacked_data[0] - 1)
                print("[Server]:return value: %d "% (record))# must encode a string to bytes
                s = struct.Struct('!' + 'i')							# ! is network order
                ret_data = s.pack(record)
                time.sleep(5)
                self.client.send(ret_data)
        finally:
            self.lock.release()
            self.client.close()
            self.Socket.close()
            return
    
    def unpack(self,msg):
        client_msg = msg
        print(msg)
        # print('Received value : ', binascii.hexlify(client_msg))
        # Unpack data
        s = struct.Struct('!' + 'i')							# ! is network order (receive format is network order)
        unpacked_data = s.unpack(client_msg)
        # print('The data you receive:\n Integer=%d' %(unpacked_data[0]))
    
    def clientReceive(self):
        if 's' in self.control:
            self.Socket.close()
            return
        ret_data = self.Socket.recv(self.BUF_SIZE)
        s = struct.Struct('!' + 'i')
        ret_data = s.unpack(ret_data)	
        print("[Client]:Return num:"+str(ret_data[0]))
        # if ret_data[0] == 0:
        #     self.Socket.shutdown(2)
        #     self.Socket.close()
        return ret_data[0]

            
    def reinit(self):
        self.__init__(self.PORT)
        