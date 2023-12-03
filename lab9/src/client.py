import sys
import socket
import struct
import time

MULTICAST_GROUP = "225.6.7.8"
backlog = 5
BUFF_SIZE = 1024


class BR:
    def __init__(self):
        self.sendtarget = (MULTICAST_GROUP, 8888)
        self.sendsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sendsock.settimeout(5)
        self.sendttl = struct.pack("b", 1)
        self.sendsock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.sendttl
        )
        self.recvsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.recvsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.recvport = 9999
        self.recvsock.bind(("", self.recvport))
        self.recvsock.settimeout(5)
        self.JoinGroup(True)

    def JoinGroup(self, flag):  # flag = True (join) / False (leave)
        group = socket.inet_aton(self.sendtarget[0])
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        if flag:
            cmd = socket.IP_ADD_MEMBERSHIP
        else:
            cmd = socket.IP_DROP_MEMBERSHIP

        self.recvsock.setsockopt(socket.IPPROTO_IP, cmd, mreq)

    def send(self, message):
        print('sending "%s"' % message)
        sent = self.sendsock.sendto(message.encode("utf-8"), self.sendtarget)

    def recv(self):
        try:
            print("Waiting to receive message...")
            data, (rip, rport) = self.recvsock.recvfrom(BUFF_SIZE)
            msg = (
                "Receive messgae: "
                + data.decode("utf-8")
                + ",from IP: "
                + str(rip)
                + " port: "
                + str(rport)
            )
            print(data.decode("utf-8"))
        except socket.timeout:
            print("Timed out, no more responses")


if __name__ == "__main__":
    s = BR()
    s.recv()
