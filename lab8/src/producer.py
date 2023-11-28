import sys
import socket
import struct

BUF_SIZE = 1024


class Produer:
    def __init__(self, port):
        self.serverIP = socket.gethostbyname("127.0.0.1")
        self.port = int(port)
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((self.serverIP, self.port))
        self.cSocket.setblocking(False)

    def send(self, num):
        try:
            s = struct.Struct("!" + "i")
            record = num
            packed_data = s.pack(record)
            self.cSocket.send(packed_data)
        except BlockingIOError:
            pass

    def receive(self):
        try:
            server_reply = self.cSocket.recv(BUF_SIZE)
            s = struct.Struct("!" + "10s")
            unpack_data = s.unpack(server_reply)
            print(unpack_data[0].decode("utf-8"))
        except BlockingIOError:
            pass

    def close(self):
        self.cSocket.close()


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
    p = Produer(8880)
    p.send(1)
    p.receive()
    p.close()
