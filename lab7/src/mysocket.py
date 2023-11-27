import sys
import socket
import struct
import binascii
import ssl
import os

SERVER_CERT = os.path.dirname(__file__) + "/server.crt"
SERVER_KEY = os.path.dirname(__file__) + "/server.key"
CLIENT_CERT = os.path.dirname(__file__) + "/client.crt"
CLIENT_KEY = os.path.dirname(__file__) + "/client.key"


class Mysocket:
    def __init__(
        self,
        PORT=6666,
        BUF_SIZE=1024,
        serverIP="",
        backlog=5,
    ):
        self.BUF_SIZE = BUF_SIZE
        if serverIP == "":
            self.srvSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.srvSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.srvSocket.bind(("", PORT))
            self.srvSocket.listen(backlog)
            self.ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            self.ctx.verify_mode = ssl.CERT_REQUIRED
            self.ctx.load_cert_chain(certfile=SERVER_CERT, keyfile=SERVER_KEY)
            self.ctx.load_verify_locations(cafile=CLIENT_CERT)

        else:
            self.ctx = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT
            )
            self.ctx.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
            self.cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ssl_conn = self.ctx.wrap_socket(
                self.cSocket, server_side=False, server_hostname="127.0.0.1"
            )
            self.ssl_conn.connect((serverIP, PORT))

    def accept(self):
        print("Waiting for client...")
        self.client, (rip, rport) = self.srvSocket.accept()
        print("Client connect from %s:%s" % (str(rip), str(rport)))

    def ssl_receive(self):
        try:
            print("Waiting for client...")
            self.client, (rip, rport) = self.srvSocket.accept()
            print("Client connect from %s:%s" % (str(rip), str(rport)))
            ssl_conn = self.ctx.wrap_socket(self.client, server_side=True)
            # print("SSL established. Peer certificate: " + str(ssl_conn.getpeercert()))
            # print("Cipher be used:" + str(ssl_conn.cipher()))
            client_msg = ssl_conn.recv(self.BUF_SIZE)
            client_msg = int(client_msg.decode("utf-8"))
            # if client_msg < 0:
            #     self.srvSocket.close()
            #     return
            client_msg = client_msg - 1
            ssl_conn.send(str(client_msg).encode("utf-8"))
            print("Server reply: " + str(client_msg))
        except KeyboardInterrupt:
            print("Server exit!!")
        except Exception as e:
            print("SSL error" + str(e))
        return client_msg

    def ssl_send(self, msg):
        self.ssl_conn.send(str(msg).encode("utf-8"))

    def client_recv(self):
        print("Waiting for server reply...")
        server_reply = self.ssl_conn.recv(self.BUF_SIZE)
        server_reply = server_reply.decode("utf-8")
        # print(server_reply)
        return int(server_reply)

    def send(self, num, control="#"):
        # if num == 0:
        #     self.ssl_conn.close()
        #     return
        self.control = control
        record = (num, control.encode("utf-8"))  # must encode a string to bytes
        s = struct.Struct("!" + "i 5s")  # ! is network order
        self.packed_data = s.pack(*record)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            print("[Client]:Send: %d" % num)
            self.ssl_conn.send(self.packed_data)
        except socket.error as e:
            print("Socket error: %s" % str(e))

    def stop(self):
        num = 0
        self.control = "s"
        record = (num, self.control.encode("utf-8"))  # must encode a string to bytes
        s = struct.Struct("!" + "i 5s")  # ! is network order
        self.packed_data = s.pack(*record)
        # print('Packed value : ', binascii.hexlify(self.packed_data))
        try:
            self.cSocket.send(self.packed_data)
        except socket.error as e:
            print("Socket error: %s" % str(e))

    def listenPort(self):
        self.Socket.bind(("", self.PORT))
        self.Socket.listen(self.backlog)
        print("[Server]:Starting up server on port: %s" % (self.PORT))
        print("[Server]:Waiting to receive message")

    def serverReceive(self):
        while True:
            print("[Server]:Waiting for client...")
            self.client, (rip, rport) = self.srvSocket.accept()
            print("[Server]:Connect from %s:%s" % (str(rip), str(rport)))
            ssl_conn = self.ctx.wrap_socket(self.client, server_side=True)
            info = ssl_conn.getpeercert()
            info = info["subject"]
            for i in info:
                print(f"[Server]:{i[0][0]} : {i[0][1]}")
            print("[Server]:Cipher be used:" + str(ssl_conn.cipher()))
            while True:
                self.client_msg = ssl_conn.recv(self.BUF_SIZE)
                client_msg = self.client_msg
                if client_msg:
                    # msg = "Receive messgae from IP: " + str(rip) + " port: " + str(rport)
                    # print(msg)
                    # print('Received value : ', binascii.hexlify(client_msg))
                    # Unpack data
                    s = struct.Struct(
                        "!" + "i 5s"
                    )  # ! is network order (receive format is network order)
                    unpacked_data = s.unpack(client_msg)
                    print("[Server]:Receive Integer = %d" % (unpacked_data[0]))
                    if unpacked_data[0] <= 0:
                        ssl_conn.close()
                        self.srvSocket.close()
                        break
                    record = int(unpacked_data[0] - 1)
                    print(
                        "[Server]:return value: %d " % (record)
                    )  # must encode a string to bytes
                    s = struct.Struct("!" + "i")  # ! is network order
                    ret_data = s.pack(record)
                    ssl_conn.send(ret_data)
                    if record <= 0:
                        ssl_conn.close()
                        self.srvSocket.close()
                        break
            break

    def unpack(self, msg):
        client_msg = msg
        print(msg)
        # print('Received value : ', binascii.hexlify(client_msg))
        # Unpack data
        s = struct.Struct(
            "!" + "i"
        )  # ! is network order (receive format is network order)
        unpacked_data = s.unpack(client_msg)
        # print('The data you receive:\n Integer=%d' %(unpacked_data[0]))

    def clientReceive(self):
        if "s" in self.control:
            self.ssl_conn.close()
            return
        ret_data = self.ssl_conn.recv(self.BUF_SIZE)
        s = struct.Struct("!" + "i")
        ret_data = s.unpack(ret_data)
        print("[Client]:Return num:" + str(ret_data[0]))
        # if ret_data[0] == 0:
        #     self.Socket.shutdown(2)
        #     self.Socket.close()
        return ret_data[0]


if __name__ == "__main__":
    s = Mysocket()
    msg = s.ssl_receive()
