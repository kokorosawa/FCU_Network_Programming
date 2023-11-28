import sys
import socket
import select
import struct
import time

BUF_SIZE = 1024


class Customer:
    def __init__(self, port):
        self.serverIP = socket.gethostbyname("127.0.0.1")
        self.port = int(port)
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((self.serverIP, self.port))
        self.cSocket.setblocking(False)

    def send(self):
        s = struct.Struct("!" + "10s")
        packed_data = s.pack("Request".encode("utf-8"))
        self.cSocket.send(packed_data)

    def receive(self):
        try:
            server_reply = self.cSocket.recv(BUF_SIZE)
            s = struct.Struct("!" + "i 5s")
            unpack_data = s.unpack(server_reply)
            if "OK" in unpack_data[1].decode("utf-8"):
                print("OK")
                print(unpack_data[0])
                return unpack_data[1].decode("utf-8")
            elif "ERROR" in unpack_data[1].decode("utf-8"):
                print(unpack_data[1].decode("utf-8"))
                return None
        except BlockingIOError:
            print("Waiting")

    def close(self):
        self.cSocket.close()


if __name__ == "__main__":
    c = Customer(8881)
    c.send()
    # c.receive()
    while True:
        if c.receive() != None:
            break
        time.sleep(2)
    c.close()
