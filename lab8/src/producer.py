import sys
import socket

BUF_SIZE = 1024


def main(port):
    # Get server IP
    serverIP = socket.gethostbyname("127.0.0.1")
    port = int(port)

    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    cSocket.connect((serverIP, port))

    # Send message to server
    msg = "Client hello!!"
    cSocket.send(msg.encode("utf-8"))

    # Receive server reply, buffer size = 1024
    server_reply = cSocket.recv(BUF_SIZE)
    print(server_reply.decode("utf-8"))

    # Close the TCP socket
    cSocket.close()


# end of main


if __name__ == "__main__":
    main(8880)
