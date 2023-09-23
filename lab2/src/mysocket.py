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
        
        
    def send(self,num,control ='#'):
        self.control = control
        record = (num, control.encode('utf-8'))		# must encode a string to bytes
        s = struct.Struct('!' + 'i 5s')							# ! is network order
        self.packed_data = s.pack(*record)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            print('Send: %d' % num)
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
        print('Starting up server on port: %s' % (self.PORT))
        print('Waiting to receive message from client')
        
    def serverReceive(self):
        while True:
            client, (rip, rport) = self.Socket.accept()
            while True:
                self.client_msg = client.recv(self.BUF_SIZE)
                client_msg = self.client_msg
                if client_msg:
                    # msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
                    # print(msg)
                    # print('Received value : ', binascii.hexlify(client_msg))
                    # Unpack data
                    s = struct.Struct('!' + 'i 5s')# ! is network order (receive format is network order)
                    unpacked_data = s.unpack(client_msg)
                    print('The data you receive: Integer=%d string: %s' %(unpacked_data[0],unpacked_data[1].decode('utf-8')))
                    if 's' in unpacked_data[1].decode('utf-8') or unpacked_data[0] == 0:
                        print("stop")
                        client.close()
                        self.Socket.close()
                        return
                    record = int(unpacked_data[0] - 1)
                    print("return value: %d "% (record))# must encode a string to bytes
                    s = struct.Struct('!' + 'i')							# ! is network order
                    ret_data = s.pack(record)
                    client.send(ret_data)
    
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
        print("return num:"+str(ret_data[0]))
        # if ret_data[0] == 0:
        #     self.Socket.shutdown(2)
        #     self.Socket.close()
        return ret_data[0]

            
    def reinit(self):
        self.__init__(self.PORT)
        