import sys
import socket
import select
import struct
import threading

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
            print("Listening on port " + str(i))

    def waiting(self):
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            # print("readable: ", readable)
            for s in readable:
                print("readable: ", s.getsockname()[1])
                # print("srv_list: ", srv_list)
                if s in srv_list:  # new connection
                    # Accept the incomming connection
                    connection, (rip, rport) = s.accept()
                    # Set the connection non blocking
                    connection.setblocking(False)
                    # Add connection to inputs (listen message on the connection)
                    inputs.append(connection)
                    laddr = connection.getsockname()
                    msg = "Accept connection on port: %d from (%s, %d)" % (
                        laddr[1],
                        str(rip),
                        rport,
                    )
                    print(msg)
                else:  # receive data
                    try:
                        print("quene: ", q)
                        data = s.recv(BUF_SIZE)
                        if data:
                            if s.getsockname()[1] == 8880:
                                print("Producer")
                                fmt = struct.Struct("!" + "i")
                                unpacked_data = fmt.unpack(data)
                                print(unpacked_data)
                                if len(q) < 5:
                                    q.append(unpacked_data[0])
                                    print(f"quene append {msg}\n")
                                    msg = "OK"
                                    fmt = struct.Struct("!" + "10s")
                                    packed_data = fmt.pack(msg.encode("utf-8"))
                                    s.send(packed_data)
                                    s.close()
                                else:
                                    msg = "ERROR"
                                    fmt = struct.Struct("!" + "10s")
                                    packed_data = fmt.pack(msg.encode("utf-8"))
                                    s.send(packed_data)
                                    s.close()
                            elif s.getsockname()[1] == 8881:
                                print("Consumer")
                                fmt = struct.Struct("!" + "10s")
                                unpacked_data = fmt.unpack(data)
                                print(unpacked_data[0].decode("utf-8"))
                                if len(q) > 0:
                                    msg = q.pop()
                                    print(f"quene pop {msg}\n")
                                    fmt = struct.Struct("!" + "i 5s")
                                    msg = (msg, "OK".encode("utf-8"))
                                    packed_data = fmt.pack(*msg)
                                    s.send(packed_data)
                                    s.close()
                                elif len(q) == 0:
                                    print("quene is empty")
                                    msg = 0
                                    fmt = struct.Struct("!" + "i 5s")
                                    packed_data = (msg, "ERROR".encode("utf-8"))
                                    packed_data = fmt.pack(*packed_data)
                                    s.send(packed_data)
                            # Send message to client
                            inputs.remove(s)
                    except ConnectionResetError:
                        print("Connection reset by peer")
                        pass
            # end for readable

            for s in exceptional:
                print("Close : ", s)
                inputs.remove(s)
                s.close()


if __name__ == "__main__":
    portlist = [8880, 8881]
    srv = Server(portlist)
    srv.waiting()
