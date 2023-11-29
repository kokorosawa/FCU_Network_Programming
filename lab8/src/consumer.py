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

    def connect(self):
        self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cSocket.connect((self.serverIP, self.port))
        self.cSocket.setblocking(False)

    def send(self):
        s = struct.Struct("!" + "10s")
        packed_data = s.pack("Request".encode("utf-8"))
        self.cSocket.send(packed_data)

    def receive(self):
        try:
            time.sleep(0.5)
            server_reply = self.cSocket.recv(BUF_SIZE)
            if server_reply == b"":
                self.cSocket.close()
                print("Server close")
                return None
            else:
                s = struct.Struct("!" + "i 5s")
                unpack_data = s.unpack(server_reply)
                if "OK" in unpack_data[1].decode("utf-8"):
                    print("[Consumer]:OK")
                    print(f"[Consumer]:{unpack_data[0]}")
                    return unpack_data[1].decode("utf-8")
                elif "ERROR" in unpack_data[1].decode("utf-8"):
                    # print(unpack_data[1].decode("utf-8"))
                    print("[Consumer]:Waiting")
                    return None
        except BlockingIOError:
            print("Waiting")
            return None

    def close(self):
        self.cSocket.close()


def consumer_task():
    c = Customer(8881)
    c.connect()
    c.send()
    while True:
        if c.receive() != None:
            break
        c.close()
        c.connect()
        c.send()
        time.sleep(2)
    c.close()


if __name__ == "__main__":
    consumer_task()
