import MySAWSocket

PORT = 8888
BUF_Size = 1024


def main():
    # Create a SAWSocket Server
    server = MySAWSocket.SAWSocket(8888)  # Listen on port 8888
    server.accept()
    sliding_window_buffer = []
    sliding_window_index = 1
    sliding_window_counter_slow = 0
    sliding_window_counter_fast = server.sliding_window_size - 1

    for i in range(10):
        msg = server.receive()
        print("Receive message: " + msg.decode("utf-8"))

    while True:
        try:
            msg = server.receive()
            sliding_window_buffer.append(msg)
            if len(sliding_window_buffer) == server.sliding_window_size:
                for i in range(len(sliding_window_buffer)):
                    print("Receive message: " + sliding_window_buffer[i])
                sliding_window_buffer = []
                sliding_window_counter_slow += server.sliding_window_size
                sliding_window_counter_fast += server.sliding_window_size
                server.replyACK(sliding_window_counter_slow + 1)
        except Exception as e:
            msg = server.receive()


# end of main

if __name__ == "__main__":
    main()
