import socket
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def main():
    while True:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        
        command = print_list_of_commands()
        client.sendall(bytes(command, "utf-8"))

        data = client.recv(1024).decode('utf-8')
        if not data:
            break
        print(f'{data}\n')



def print_list_of_commands():
    print('\n-------------------- Waiting for new commands --------------------')
    print("List of Commands:")
    print("[1] List sorting. How to use: sort [list]")
    print("[2] Book search. How to use: book_search \"Harry_potter\". Note: book title in quotes and separated with underscores (_)")
    print("[3] Generate n-th fibonnaci number. How to use: fibonacci n")
    command = input("Input command: ")
    return command


if __name__ == '__main__':
    main()