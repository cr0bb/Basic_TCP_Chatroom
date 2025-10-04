import threading
import socket
import time
import logging
import sys

host = '127.0.0.1' # localhost
port = 45547

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

                    ##################### LOGGING ######################

def setup_info_logger(name, log_file, formatter):
    handler = logging.FileHandler(log_file)
    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    return logger

chat_format = logging.Formatter(fmt='%(asctime)s - %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
activity_format = logging.Formatter(fmt='%(asctime)s --> %(message)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
chat_logger = setup_info_logger('chat_logger', 'chats.log', chat_format)
activity_logger = setup_info_logger('activity_logger', 'activity.log', activity_format)

                    ####################################################


                    ##################### HANDLING #####################

# Closes a client connection and removes them from the lists
def closeC(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        activity_logger.info(f'{nickname} disconnected')
        broadcast(f"\033[1m{nickname}\033[0m left the chat.".encode('ascii'))
        print(f"\033[1m{nickname}\033[0m disconnected")
        nicknames.remove(nickname)
        sys.exit()

# Broadcasts a message to the chatroom
def broadcast(message):
    for client in clients:
        client.send(message)

                    ####################################################


                    ##################### COMMANDS #####################

# Kicks a user from the chatroom
def kick_user(name):
    if name in nicknames:
        i = nicknames.index(name)
        client = clients[i]
        clients.remove(client)
        client.send("You have been kicked.".encode('ascii'))
        client.close()
        nicknames.remove(name)
        activity_logger.info(f'{name} kicked by ADMIN')
        broadcast(f'\033[1m{name}\033[0m was kicked.'.encode('ascii'))
        print(f'\033[1m{name}\033[0m was disconnected by ADMIN.')
    else:
        clients[nicknames.index('ADMIN')].send("User not found.".encode('ascii'))

# Changes the password of the admin account in password.txt
def changepw(password):
    with open('password.txt', 'w') as f:
        f.write(password)

# Clears the logs of the chatroom
def clear_logs(log_file):
    with open(log_file, 'w') as f:
        pass

def read_n_logs(log_file, n):
    with open(log_file, 'r') as f:
        logs = f.readlines()
        last = logs[-n:]

    res = ''
    for log in last:
        res += log
    return res

                    ####################################################

# Handles messages from clients and deletes clients when their connection closes
# 'msg' handles commands, 'message' handles broadcasting
def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)

            # KICK
            if msg.decode('ascii').startswith('KICK'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    name_to_kick = msg.decode('ascii')[5:]
                    clients[nicknames.index(name_to_kick)].send('KICKED'.encode('ascii'))
                    kick_user(name_to_kick)
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))

            # BAN
            elif msg.decode('ascii').startswith('BAN'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    name_to_ban = msg.decode('ascii')[4:]
                    kick_user(name_to_ban)
                    with open('bans.txt', 'a') as file:
                        file.write(f'{name_to_ban}\n')
                    print(f'\033[1m{name_to_ban} was banned from the server\033[0m')
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))

            # PASSWORD CHANGE/VIEW
            elif msg.decode('ascii').startswith('PWC'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    client.send("Enter new password: ".encode('ascii'))
                    new_password = client.recv(1024).decode('ascii')[len(nicknames[clients.index(client)])+2:]
                    with open('password.txt', 'r') as f:
                        curr_password = f.read()
                    if new_password == curr_password:
                        client.send("Password cannot be old password".encode('ascii'))
                        continue
                    elif new_password == '':
                        client.send("Password cannot be empty".encode('ascii'))
                        continue
                    else:
                        changepw(new_password)
                        client.send("Password change successful".encode('ascii'))
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))
            elif msg.decode('ascii').startswith('PWV'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    with open('password.txt', 'r') as f:
                        curr_password = f.read()
                    client.send(curr_password.encode('ascii'))
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))

            # LOGS
            elif msg.decode('ascii').startswith('CLOGS'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    logs = read_n_logs("chats.log", int(msg.decode("ascii")[6:]))
                    client.send(logs.encode('ascii'))
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))
            elif msg.decode('ascii').startswith('ALOGS'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    logs = read_n_logs("activity.log", int(msg.decode("ascii")[6:]))
                    client.send(logs.encode('ascii'))
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))

            # CLEAR LOGS
            elif msg.decode('ascii').startswith('CLEARLOGS'):
                if nicknames[clients.index(client)] == 'ADMIN':
                    if msg.decode('ascii')[10:] == 'a':
                        clear_logs('activity.log')
                        client.send("All activity logs cleared".encode('ascii'))
                    elif msg.decode('ascii')[10:] == 'c':
                        clear_logs('chats.log')
                        client.send("All chat logs cleared".encode('ascii'))
                    else:
                        client.send("Invalid command".encode('ascii'))
                else:
                    client.send("Invalid permissions to use command".encode('ascii'))

            # QUIT
            elif msg.decode('ascii') == 'QUIT':
                client.send("Goodbye!".encode('ascii'))
                time.sleep(1)
                closeC(client)
                break

            # LIST
            elif msg.decode('ascii') == 'LIST':
                client.send(f'Users connected to the chat: \033[1m{str(nicknames)}\033[0m'.encode('ascii'))

            # HELP
            elif msg.decode('ascii') == 'HELP':
                if nicknames[clients.index(client)] == 'ADMIN':
                    client.send("\nAvailable commands:\n"
                                "\033[1m/alogs [n]               -\033[0m Display the last \033[1mn\033[0m activity logs\n"
                                "\033[1m/ban [nickname]          -\033[0m Ban a user from the chatroom\n"
                                "\033[1m/clearlogs [ 'c' / 'a' ] -\033[0m Clear all chat or activity logs\n"
                                "\033[1m/clogs [n]               -\033[0m Display the last \033[1m[n]\033[0m chat logs\n"
                                "\033[1m/help                    -\033[0m Displays a list of commands you're able to use\n"
                                "\033[1m/kick [nickname]         -\033[0m Kick a user from the chatroom\n"
                                "\033[1m/list                    -\033[0m Displays a list of all users connected to the chatroom\n"
                                "\033[1m/pw [ 'c' / 'v' ]        -\033[0m Change or view the password of the server\n"
                                "\033[1m/quit             -\033[0m Leave the chatroom\n".encode('ascii'))
                else:
                    client.send("\nAvailable commands:\n"
                                "\033[1m/help -\033[0m Displays a list of commands you're able to use\n"
                                "\033[1m/list -\033[0m Displays a list of all users connected to the chatroom\n"
                                "\033[1m/quit -\033[0m Leave the chatroom\n".encode('ascii'))
            elif msg.decode('ascii') == '':
                continue
            else:
                broadcast(message)
                chat_logger.info(f'{msg.decode("ascii")}'.strip())
        except:
            closeC(client)
            sys.exit()

# Accepts clients constantly, server admin is notified of new connections
# Send keyword "NICK" to client for nickname input, check if client is banned.
# Start thread handling separate client connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))

        nickname = client.recv(1024).decode('ascii')


        with open('bans.txt', 'r') as f:
            bans = f.readlines()

        if nickname+'\n' in bans:
            client.send('BANNED'.encode('ascii'))
            client.close()
            continue

        if nickname in nicknames:
            client.send('NICKNAME_TAKEN'.encode('ascii'))
            client.close()
            continue

        if nickname == "ADMIN":
            if nickname in nicknames:
                client.send('NICKNAME_TAKEN'.encode('ascii'))
                client.close()
                continue
            else:
                client.send('PASS'.encode('ascii'))
                password = client.recv(1024).decode('ascii').strip()

            with open('password.txt', 'r') as f:
                curr_password = f.read()

            if password != curr_password:
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue

        nicknames.append(nickname)
        clients.append(client)
        activity_logger.info(f'{nickname} connected at {address}')

        broadcast(f"\033[1m{nickname}\033[0m joined the chat.".encode('ascii'))
        if nickname != 'ADMIN':
            client.send("Connected to the server\n"
                    "\033[1mWelcome to the chatroom!\033[0m Type '/help' for commands".encode('ascii'))
            print(f'Nickname of the client is \033[1m{nickname}\033[0m')
        else:
            client.send("Connected to the server\n"
                        "\033[1mWelcome ADMIN.\033[0m".encode('ascii'))
            print(f'\033[1mADMIN\033[0m Connected')

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


## RUNNABLE ##
if __name__ == '__main__':
    print("Server is listening...")
    receive()
