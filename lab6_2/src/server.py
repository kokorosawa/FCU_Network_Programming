import MySAWSocket

PORT = 8888
BUF_Size = 1024

def main():
	# Create a SAWSocket Server 
	server = MySAWSocket.SAWSocket(8888)		# Listen on port 8888
	server.accept()
	
	for i in range(10):
		msg = server.receive()
		print('Receive message: ' + msg.decode('utf-8'))
	
	server.close()
# end of main

if __name__ == '__main__':
	main()