import socket
import threading
import time
import Queue
import addr_list
import spy_grid

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ADDR = (SERVER, PORT)
server.bind(ADDR)



def main():
    print('[STARTING] server is starting...')

    comm_queue = Queue.Queue()
    connected_players = start_player_search(comm_queue)
    grid_adt = spy_grid.Grid(canvas=None, server=True)
    for player in range(connected_players.get_size()):
        grid_adt.add_agent()
        export_str = grid_adt.export_to_str()
    distribute_messages(connected_players, export_str)


def distribute_messages(connections, msg):
    print(msg)
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
