import sys
import socket
import select
import struct
import threading
import time

inputs = []
srv_list = []
outputs = []
q = []
BUF_SIZE = 1024


class Server:
    def __init__(self, portlist):
        for i in portlist:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("", i))
            self.socket.setblocking(False)
            self.socket.listen(5)
            inputs.append(self.socket)
            srv_list.append(self.socket)
            print("[Server]:Listening on port " + str(i))

    def waiting(self):
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            # print("readable: ", readable)
            for s in readable:
                # print("srv_list: ", srv_list)
                if s in srv_list:  # new connection
                    # Accept the incomming connection
                    connection, (rip, rport) = s.accept()
                    # Set the connection non blocking
                    connection.setblocking(False)
                    # Add connection to inputs (listen message on the connection)
                    print("[Server]:connection: ", connection.getsockname())
                    inputs.append(connection)
                    laddr = connection.getsockname()
                else:  # receive data
                    try:
                        data = s.recv(BUF_SIZE)
                        if data:
                            if s.getsockname()[1] == 8880:
                                fmt = struct.Struct("!" + "i")
                                unpacked_data = fmt.unpack(data)
                                num = unpacked_data[0]
                                if len(q) < 5:
                                    q.append(num)
                                    print(f"[Server]:Quene append {num}")
                                    msg = "OK"
                                    fmt = struct.Struct("!" + "10s")
                                    packed_data = fmt.pack(msg.encode("utf-8"))
                                    s.send(packed_data)
                                    # s.close()
                                else:
                                    msg = "ERROR"
                                    fmt = struct.Struct("!" + "10s")
                                    packed_data = fmt.pack(msg.encode("utf-8"))
                                    s.send(packed_data)
                                    # s.close()
                            elif s.getsockname()[1] == 8881:
                                fmt = struct.Struct("!" + "10s")
                                unpacked_data = fmt.unpack(data)
                                print(unpacked_data[0].decode("utf-8"))
                                if len(q) > 0:
                                    msg = q.pop()
                                    print(f"[Server]: Quene pop {msg}\n")
                                    fmt = struct.Struct("!" + "i 5s")
                                    msg = (msg, "OK".encode("utf-8"))
                                    packed_data = fmt.pack(*msg)
                                    s.send(packed_data)
                                    # s.close()
                                elif len(q) == 0:
                                    print("[Server]:Quene is empty")
                                    msg = 0
                                    fmt = struct.Struct("!" + "i 5s")
                                    packed_data = (msg, "ERROR".encode("utf-8"))
                                    packed_data = fmt.pack(*packed_data)
                                    s.send(packed_data)
                                    # s.close()
                            # Send message to client
                            inputs.remove(s)
                        print(f"[Queue]: {q}")
                    except ConnectionResetError:
                        print(f"[Server]:Connection reset by peer")
                        pass
            # end for readable

            for s in exceptional:
                print("Close : ", s)
                inputs.remove(s)
                # s.close()


def server_task():
    portlist = [8880, 8881]
    srv = Server(portlist)
    srv.waiting()


if __name__ == "__main__":
    server_task()
