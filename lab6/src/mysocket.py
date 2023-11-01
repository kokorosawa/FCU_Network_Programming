import sys
import socket
import struct
import binascii
import time
import random

class Mysocket:
    def __init__(self,PORT=6666, BUF_SIZE=1024,serverIP='127.0.0.1',backlog=5):
        self.PORT = PORT
        self.BUF_SIZE = BUF_SIZE
        self.backlog = backlog
        self.serverIP = socket.gethostbyname(serverIP)
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def send(self,num,control ='#'):
        self.control = control	# must encode a string to bytes
        s = struct.Struct('!' + 'I')						# ! is network order
        self.packed_data = s.pack(num)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            print('[Client]:Send: %d' % num)
            self.Socket.sendto(self.packed_data,(self.serverIP, self.PORT))
        except socket.error as e:
            print('Socket error: %s' % str(e))

    def listenPort(self):
        self.Socket.bind(('', self.PORT)) 
        print('[Server]:Starting up server on port: %s' % (self.PORT))
        print('[Server]:Waiting to receive message')
        while True:
            recv_data,( self.serverIP, self.PORT) = self.Socket.recvfrom(self.BUF_SIZE)
            s = struct.Struct('!' + 'I')
            unpacked_data = s.unpack(recv_data)
            print('[Server]:Receive Integer=%d' %(unpacked_data[0]))
            record = int(unpacked_data[0] - 1)
            print("[Server]:return value: %d "% (record))# must encode a string to bytes
            s = struct.Struct('!' + 'i')	
            ret_data = s.pack(record)
            random.seed(time.time())
            # bad = random.randint(0, 10)
            # if bad % 3 == 0:
            #     time.sleep(1)
            self.Socket.sendto(ret_data,(self.serverIP, self.PORT))
            if(record == 0):
                break
        self.Socket.close()
        print('[Server]:Close the socket')
            
    
    def clientRecv(self):
        # self.Socket.connect((self.serverIP, self.PORT))
        raw_data, (rip, rport) = self.Socket.recvfrom(self.BUF_SIZE)
        s = struct.Struct('!' + 'I')
        unpacked_data = s.unpack(raw_data)
        print('[Client]:Receive Integer=%d' %(unpacked_data[0]))
        return unpacked_data[0]