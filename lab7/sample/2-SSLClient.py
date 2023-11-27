####################################################
#  Network Programming - Unit 6 Secure Socket
#  Program Name: 2-SSLClient.py
#  The program verify the server certificate.
#  2021.07.28
####################################################
import sys
import socket
import ssl
import os

PORT = 6666
recv_buff_size = 1024  # Receive buffer size
SERVER_CERT = os.path.dirname(__file__) + "/server.crt"
SERVER_KEY = os.path.dirname(__file__) + "/server.key"
CLIENT_CERT = os.path.dirname(__file__) + "/client.crt"
CLIENT_KEY = os.path.dirname(__file__) + "/client.key"


def main():
    # Get server IP
    serverIP = socket.gethostbyname("127.0.0.1")

    # Verify server Certificate
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=SERVER_CERT)
    ctx.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

    # Create a TCP client socket
    cSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Wrap socket
    ssl_conn = ctx.wrap_socket(cSocket, server_side=False, server_hostname="127.0.0.1")

    # Connect to server
    print("Connecting to %s port %s" % (serverIP, PORT))
    try:
        ssl_conn.connect((serverIP, PORT))
        print("SSL established. Peer certificate: " + str(ssl_conn.getpeercert()))

        # Send message to server
        msg = "Application data from client!!"
        ssl_conn.send(msg.encode("utf-8"))
        msg = "Application data from client 2 !!"
        ssl_conn.send(msg.encode("utf-8"))
    except:
        print("SSL error")

    print("Closing connection.")
    # Close the SSL socket
    # ssl_conn.close()


# end of main


if __name__ == "__main__":
    main()
