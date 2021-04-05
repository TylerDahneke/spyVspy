import socket
import threading
import time
import Queue
import addr_list

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
server.bind(ADDR)

InputGrid = '0.0. 100.0. 200.0. 300.0. 400.0. 500.0._0.100. 100.100. 200.100. 300.100. 400.100.blue.red. 500.100._0.200. ' \
            '100.200. 200.200. 300.200. 400.200. 500.200._0.300.red.0. 100.300. 200.300. 300.300. 400.300. ' \
            '500.300._0.400. 100.400. 200.400.green.1. 300.400. 400.400. 500.400._0.500. 100.500. 200.500. 300.500. 400.500. ' \
            '500.500._ '


def main():
    print('[STARTING] server is starting...')

    comm_queue = Queue.Queue()
    connected_players = start_player_search(comm_queue)

    distribute_messages(connected_players, InputGrid)


def distribute_messages(connections, msg):
    for client in connections.contents:
        print(f'sent to {client}')
        client.conn.send(msg.encode(FORMAT))


def handle_client(comm_queue, conn, addr):
    print(f"[NEW CONNECTIONS] {addr} connected")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                comm_queue.insert(msg)
    conn.close()


def start_player_search(comm_queue):
    server.listen()
    connection_list = addr_list.conn_list()
    print(f'[LISTENING] Server is listening on {SERVER}')
    while connection_list.get_size() < 2:
        conn, addr = server.accept()
        connection_list.insert(conn, addr)
        thread = threading.Thread(target=handle_client, args=(comm_queue, conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {connection_list.get_size()}")
    return connection_list


if __name__ == '__main__':
    main()
