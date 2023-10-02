####################################################
#  Network Programming - Unit 3 Application based on TCP         
#  Program Name: pop3client.py                                      			
#  The program is a simple POP3 client.            		
#  2021.08.03                                                   									
####################################################
import sys
import socket
from getpass import getpass

PORT = 110
BUFF_SIZE = 1024			# Receive buffer size

def ParseMessage(msg):
	line = []
	newstring = ''
	for i in range(len(msg)):
		if(msg[i] == '\n'):
			line.append(newstring)
			newstring = ''
		else:
			newstring += msg[i]
	return line
# end ParseMessage

def main():
	# if(len(sys.argv) < 2):
	# 	print("Usage: python3 pop3client.py ServerIP")
	# 	exit(1)

	# Get server IP
	serverIP = socket.gethostbyname('140.134.135.41')
	
	# Get username & password
	# name = input('Username: ')
	# password = getpass('Password: ') 
	name = 'iecs07'
	password = '3SmUnqYy'
	
 
	# Create a TCP client socket
	cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print('Connecting to %s port %s' % (serverIP, PORT))
	cSocket.connect((serverIP, PORT))
	
	for i in range(1):
		try:
			# receive server greeting message
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print('Receive message: %s' % reply)
			if(reply[0] != '+'):
				break
				
			# Username
			cmd = 'USER ' + name + '\r\n'			# don't forget "\r\n"
			cSocket.send(cmd.encode('utf-8'))
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print('Receive message: %s' % reply)
			if(reply[0] != '+'):
				break

			# Password
			cmd = 'PASS ' + password + '\r\n'	# don't forget "\r\n"\
			cSocket.send(cmd.encode('utf-8'))
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print('Receive message: %s' % reply)
			if(reply[0] != '+'):
				break
			
			# List [Method 1]
			cmd = 'LIST\r\n'								# don't forget "\r\n"\
			cSocket.send(cmd.encode('utf-8'))
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print('Receive message: %s' % reply)
			if(reply[0] != '+'):
				break
			# Count mails
			line = ParseMessage(reply)
			num = len(line) - 2
			print('Mailbox has %d mails\n' % num)
   
			cmd = "RETR " + str(num) + "\r\n"
			cSocket.send(cmd.encode("utf-8"))
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print("text in %d:\n%s"%(num, reply))
			
			# List [Method 2]
			cmd = 'LIST\r\n'								# don't forget "\r\n"\
			cSocket.send(cmd.encode('utf-8'))
			reply = cSocket.recv(BUFF_SIZE).decode('utf-8')
			print('Receive message: %s' % reply)
			if(reply[0] != '+'):
				break
			# Count mails
			tokens = reply.split(' ')
			print('Mailbox has %d mails' % int(tokens[1]))
		
			# Quit
			cmd = 'QUIT\r\n'								# don't forget "\r\n"\
			cSocket.send(cmd.encode('utf-8'))			
		except socket.error as e:
			print('Socket error: %s' % str(e))
		except Exception as e:
			print('Other exception: %s' % str(e))
	# end for 
	
	print('Closing connection.')
	cSocket.close()
# end of main


if __name__ == '__main__':
	main()
