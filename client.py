import socket
import threading
import time
import Queue

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "192.168.1.59"


def start():
    ADDR = (SERVER, PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(f'Connected to {SERVER}')

    comm_queue = Queue.Queue()
    while not comm_queue.get_size():
        fish(comm_queue, client)
    ph = comm_queue.pop()
    return ph


def fish(comm_queue, client):
    msg = client.recv(2048).decode(FORMAT)
    comm_queue.insert(msg)


def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
