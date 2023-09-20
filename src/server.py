import sys
import socket
import struct
import binascii

class Server:
     def __init__(self,PORT=6666,backlog=5,BUF_SIZE = 1024):
        self.srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Starting up server on port: %s' % (PORT))
        self.srvSocket.bind(('', PORT))
        self.srvSocket.listen(backlog)
        print('Waiting to receive message from client')
        client, (rip, rport) = self.srvSocket.accept()
        client_msg = client.recv(BUF_SIZE)
        if client_msg:
            msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
            print(msg)
            print('Received value : ', binascii.hexlify(client_msg))
            # Unpack data
            s = struct.Struct('!' + 'i')							# ! is network order (receive format is network order)
            unpacked_data = s.unpack(client_msg)
            print('The data you receive:\n Integer=%d\n String=%s\n Floating point=%f\n' %(unpacked_data[0], unpacked_data[1].decode('utf-8'), unpacked_data[2]))

        client.close()
        self.srvSocket.close()
    


if __name__ == '__main__':
	s = Server(6666, 5)