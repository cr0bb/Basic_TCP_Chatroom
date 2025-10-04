import socket
import threading
import getpass
import sys

global command
global stop_thread

nickname = input("Choose a nickname: ")

if nickname == 'ADMIN':
    password = input("Enter the password for ADMIN: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 45547))

stop_thread = False
inp = ""
command = False

# Receive messages from the server
def receive():
    while True:
        global stop_thread
        if stop_thread:
            sys.exit()

        try:
            message = client.recv(1024).decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                next_message = client.recv(1024).decode('ascii')
                if next_message == 'PASS':
                    client.send(password.encode('ascii'))
                    if client.recv(1024).decode('ascii') == 'REFUSE':
                        print("Connection was refused, wrong password")
                        stop_thread = True
                elif next_message == 'BANNED':
                    print("Connection refused, you are banned from this server")
                    stop_thread = True
                    
            elif message == 'NICKNAME_TAKEN':
                print("Nickname is already taken")
                client.send('NICK'.encode('ascii'))

            elif message == 'KICKED':
                print("You were kicked from the chat")
                stop_thread = True

            elif message.startswith('PWC'):
                client.recv(1024).decode('ascii')
                inp = getpass.getpass("")
                client.send(inp.encode('ascii'))

                resp = client.recv(1024).decode('ascii')
                print(resp)
            elif message.startswith('PWV'):
                curr_password = client.recv(1024).decode('ascii')
                print(f'Current password is \033[1m{curr_password}\033[0m')

            elif message.startswith('CLOGS') or message.startswith('ALOGS'):
                logs = client.recv(1024).decode('ascii')[5:]
                print(logs)

            elif message == 'LIST':
                users = client.recv(1024).decode('ascii')
                print(users)

            elif message == 'HELP':
                helpm = client.recv(1024).decode('ascii')
                print(helpm)

            elif message == 'QUIT':
                stop_thread = True

            else:
                print(message)
        except:
            print("An error occurred!")
            client.close()
            break


def write():
    while True:
        global stop_thread

        if stop_thread:
            sys.exit()

        message = f'{nickname}: {input("")}'

        if message[len(nickname)+2:].startswith('/'):
            if message[len(nickname)+2:].startswith('/kick'):
                if message[len(nickname)+2+6:].isalnum():
                    client.send(f'KICK {message[len(nickname)+2+6:]}'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/ban'):
                if message[len(nickname)+2+5:].isalnum():
                    client.send(f'BAN {message[len(nickname)+2+5:]}'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/pw'):
                if message[len(nickname)+2+4:] == 'c':
                    client.send(f'PWC'.encode('ascii'))
                elif message[len(nickname)+2+4:] == 'v':
                    client.send(f'PWV'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/alogs'):
                if message[len(nickname)+2+7:].isdigit():
                    client.send(f'ALOGS {message[len(nickname)+2+7:]}'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/clogs'):
                if message[len(nickname)+2+7:].isdigit():
                    client.send(f'CLOGS {message[len(nickname)+2+7:]}'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/clearlogs'):
                if message[len(nickname)+2+11:] == 'a' or message[len(nickname)+2+11:] == 'c':
                    client.send(f'CLEARLOGS {message[len(nickname)+2+11:]}'.encode('ascii'))
                else:
                    print("Invalid command")
            if message[len(nickname)+2:].startswith('/help'):
                client.send('HELP'.encode('ascii'))
            if message[len(nickname)+2:].startswith('/quit'):
                client.send('QUIT'.encode('ascii'))
                stop_thread = True
            if message[len(nickname)+2:].startswith('/list'):
                client.send('LIST'.encode('ascii'))
        else:
            client.send(message.encode('ascii'))


## RUNNABLE ##
if __name__ == "__main__":
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()