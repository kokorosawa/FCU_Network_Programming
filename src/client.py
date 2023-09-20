import sys
import socket
import struct
import binascii

class Client:
    def __init__(self,PORT=6666, BUF_SIZE=1024,serverIP='127.0.0.1'):
        self.PORT = PORT
        self.BUF_SIZE = BUF_SIZE
        self.serverIP = socket.gethostbyname(serverIP)
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print('Connecting to %s port %s' % (self.serverIP, self.PORT))
        self.cSocket.connect((self.serverIP, self.PORT))
        
    def packed(self):
        record = 7	# must encode a string to bytes
        # s = struct.Struct('!' + 'I 10s f')
        formatter = 'i'	
        self.packed_data = struct.pack(formatter,record)
        print('Packed value : ', binascii.hexlify(self.packed_data))
        
    def send(self):
        try:
            print('Send: %s' % self.packed_data)
            self.cSocket.send(self.packed_data)
        except socket.error as e:
            print('Socket error: %s' % str(e))

if __name__ == '__main__':
    c = Client()
    c.connect()
    c.packed()
    c.send()