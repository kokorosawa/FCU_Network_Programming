import sys
import socket
from getpass import getpass

PORT = 110
BUFF_SIZE = 1024			# Receive buffer size

class Mail:
    def __init__(self, BUFF_SIZE = 1024, USER = "iecs07", PASW = "3SmUnqYy", IP = "140.134.135.41", PORT = 110):
        self.user = USER
        self.pasw = PASW
        self.ip = socket.gethostbyname(IP)
        self.port = PORT
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((self.ip, self.port))
        
    def ParseMessage(self, msg):
        line = []
        newstring = ''
        for i in range(len(msg)):
            if(msg[i] == '\n'):
                line.append(newstring)
                newstring = ''
            else:
                newstring += msg[i]
        return line
    
    def ready(self):
        try:
            reply = self.cSocket.recv(BUFF_SIZE).decode('utf-8')
            print('Receive message: %s' % reply)
        except Exception as e:
            print(e)

    def logIn(self):
        try:
            # Username
            cmd = 'USER ' + self.user + '\r\n'			# don't forget "\r\n"
            self.cSocket.send(cmd.encode('utf-8'))
            reply = self.cSocket.recv(BUFF_SIZE).decode('utf-8')
            print('Receive message: %s' % reply)
        except Exception as e:
            print(e)
            
        try:
			# Password
            cmd = 'PASS ' + self.pasw + '\r\n'	# don't forget "\r\n"\
            self.cSocket.send(cmd.encode('utf-8'))
            reply = self.cSocket.recv(BUFF_SIZE).decode('utf-8')
            print('Receive message: %s' % reply)
        except Exception as e:
            print(e)
			# List [Method 1]
   
    def listMailNum(self):
        try:
            cmd = 'LIST\r\n'								# don't forget "\r\n"\
            self.cSocket.send(cmd.encode('utf-8'))
            reply = self.cSocket.recv(BUFF_SIZE).decode('utf-8')
            print('Receive message: %s' % reply)
            # Count mails
            line = self.ParseMessage(reply)
            num = len(line) - 2
            print('Mailbox has %d mails\n' % num)
        except Exception as e:
            print(e)
    
    def readMail(self,num):
        try:
            cmd = "RETR " + str(num) + "\r\n"
            self.cSocket.send(cmd.encode("utf-8"))
            reply = self.cSocket.recv(BUFF_SIZE).decode('utf-8')
            print("text in %d:\n%s"%(num, reply))
        except Exception as e:
            print(e)
			
    def quit(self):
        try:
            cmd = 'QUIT\r\n'								# don't forget "\r\n"\
            self.cSocket.send(cmd.encode('utf-8'))			
        except Exception as e:
            print(e)
		