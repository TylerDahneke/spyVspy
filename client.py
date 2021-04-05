import socket
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "192.168.1.70"

ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

socket.gethostname()

def fish():
    while True:
        print(client.recv(2048).decode(FORMAT))
        time.sleep(1)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

def main():
    inp = input('')
    thread = threading.Thread(target=fish)
    thread.start()
    while inp != "":
        send(inp)
        inp = input('')
    send(DISCONNECT_MESSAGE)


if __name__ == '__main__':
    main()