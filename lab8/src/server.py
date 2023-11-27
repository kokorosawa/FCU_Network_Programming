import sys
import socket
import select
import struct

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
                        data = s.recv(BUF_SIZE)
                        if data:
                            raddr = s.getpeername()
                            laddr = s.getsockname()
                            msg = (
                                "Receive messgae: "
                                + data.decode("utf-8")
                                + " on :"
                                + str(laddr)
                                + " from : "
                                + str(raddr)
                            )
                            print(msg)
                            # Send message to client
                            server_reply = "Server Reply!!"
                            s.send(server_reply.encode("utf-8"))

                            # Close connection
                            print("Close connection from: ", raddr)
                            inputs.remove(s)
                            s.close()
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
