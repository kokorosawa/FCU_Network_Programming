import MySAWSocket
import threading
import time

client = MySAWSocket.SAWSocket(8888, "127.0.0.1")
client.connect()
i = 0
lock = threading.Lock()


def send():
    try:
        lock.acquire()
        global i
        msg = "Test message " + str(i)
        client.send(msg.encode("utf-8"))
        i -= 1
    finally:
        lock.release()


def main():
    t = threading.Thread
    num = int(input("Enter number of messages to send: "))
    global i
    i = num

    while i > 0:
        sliding_window_buffer = [
            t(target=send) for _ in range(client.sliding_window_size)
        ]
        if i - client.sliding_window_size >= client.sliding_window_size:
            for s in range(client.sliding_window_size):
                sliding_window_buffer[s].start()
        else:
            for s in range(i - client.sliding_window_size):
                sliding_window_buffer[s].start()
        sliding_window_buffer = []
        time.sleep(1)
    client.close()


if __name__ == "__main__":
    main()
