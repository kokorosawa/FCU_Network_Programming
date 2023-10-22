####################################################
#  Network Programming - Unit 4 Concurrent Process
#  Program Name: 5-TCPClient.py
#  The program is a simple TCP client. (Unit 2 3-TCPClient.py)
#  2021.07.13
####################################################
import sys
import socket

PORT = 6666
BUF_SIZE = 1024			# Receive buffer size


def main():

    # Get server IP
    serverIP = socket.gethostbyname("127.0.0.1")

    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    print('Connecting to %s port %s' % (serverIP, PORT))
    cSocket.connect((serverIP, PORT))

    # Send message to server
    try:
        msg = "Client hello!!"
        cSocket.send(msg.encode('utf-8'))

        # Receive server reply, buffer size = BUF_SIZE
        server_reply = cSocket.recv(BUF_SIZE)
        print(server_reply.decode('utf-8'))
    except socket.error as e:
        print('Socket error: %s' % str(e))
    except Exception as e:
        print('Other exception: %s' % str(e))
    finally:
        print('Closing connection.')
        # Close the TCP socket
        cSocket.close()

# end of main


if __name__ == '__main__':
    for _ in range(10):
        main()
