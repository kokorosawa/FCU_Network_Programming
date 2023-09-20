import sys
import socket
import struct
import binascii

class Mysocket:
    def __init__(self,PORT, BUF_SIZE=1024,serverIP='127.0.0.1',backlog=5):
        self.PORT = PORT
        self.BUF_SIZE = BUF_SIZE
        self.backlog = backlog
        self.serverIP = socket.gethostbyname(serverIP)
        self.Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def connect(self):
        print('Connecting to %s port %s' % (self.serverIP, self.PORT))
        self.Socket.connect((self.serverIP, self.PORT))
        
        
    def send(self,num):
        record = (num)		# must encode a string to bytes
        s = struct.Struct('!' + 'I')							# ! is network order
        self.packed_data = s.pack(record)
        print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            print('Send: %s' % self.packed_data)
            self.Socket.send(self.packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))

    def listenPort(self):
        self.Socket.bind(('', self.PORT)) 
        self.Socket.listen(self.backlog)
        print('Starting up server on port: %s' % (self.PORT))
        print('Waiting to receive message from client')
        
    def serverReceive(self):
        while True:
            client, (rip, rport) = self.Socket.accept()
            self.client_msg = client.recv(self.BUF_SIZE)
            client_msg = self.client_msg
            if client_msg:
                msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
                print(msg)
                print('Received value : ', binascii.hexlify(client_msg))
                # Unpack data
                s = struct.Struct('!' + 'i')							# ! is network order (receive format is network order)
                unpacked_data = s.unpack(client_msg)
                print('The data you receive:\n Integer=%d' %(unpacked_data[0]))
                record = 6		# must encode a string to bytes
                s = struct.Struct('!' + 'I')							# ! is network order
                ret_data = s.pack(record)
                client.send(ret_data)
                client.close()
    
    def unpack(self,msg):
        client_msg = msg
        print(msg)
        print('Received value : ', binascii.hexlify(client_msg))
        # Unpack data
        s = struct.Struct('!' + 'i')							# ! is network order (receive format is network order)
        unpacked_data = s.unpack(client_msg)
        print('The data you receive:\n Integer=%d' %(unpacked_data[0]))
    
    def clientReceive(self):
        self.Socket.recv(self.BUF_SIZE)
        self.unpack(self.client_msg)
            
    def reinit(self):
        self.__init__(self.PORT)