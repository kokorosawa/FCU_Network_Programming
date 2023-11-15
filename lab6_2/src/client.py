import MySAWSocket
import threading

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
        i += 1
    finally:
        lock.release()


def main(sliding_window_size):
    sliding_window_buffer = [
        threading.Thread(target=send) for _ in range(sliding_window_size)
    ]


if __name__ == "__main__":
    t1 = threading.Thread(target=send)
    t1.start()
    t2 = threading.Thread(target=send)
    t2.start()
