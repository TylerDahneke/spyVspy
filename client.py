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

    send(client, format_pos_msg())
    comm_queue = Queue.Queue()
    while not comm_queue.get_size():
        fish(comm_queue, client)
    ph = comm_queue.pop()
    return ph


def fish(comm_queue, client):
    msg = client.recv(2048).decode(FORMAT)
    comm_queue.insert(msg)


def format_pos_msg(check=False):
    while not check:
        inp = input('Please input desired start pos:')
        if len(inp.split()) >= 2:
            check = True
        else:
            inp = input('Please input desired start pos:')
    return inp


def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
