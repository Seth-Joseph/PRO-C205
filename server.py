import socket
import shutil

SERVER = None
IP_ADDRESS = '127.0.0.1'
PORT = 6000

CLIENTS = {}
columns = shutil.get_terminal_size().columns

def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        if(len(CLIENTS.keys()) == 0):
            CLIENTS[player_name] = {'player_type': 'player1'}
        else:
            CLIENTS[player_name] = {'player_type': 'player2'}
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name
        CLIENTS[player_name]["turn"] = False

        print(f"Connection established with {player_name} : {addr}")
        print(f"Players connected:{len(CLIENTS)}")

def setup():
    print("*** Welcome To Tambola Game ***".center(columns))
    print("Stage 2".center(columns))

    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("SERVER IS WAITING FOR INCOMMING CONNECTIONS...".center(columns))

    acceptConnections()

setup()