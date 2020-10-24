import socket
import pickle
import time

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

print("Commands:")
print("[1] List sorting. How to use: sort [list]")
print("[2] Book search. How to use: book_search \"Harry_potter\". Note: book title in quotes and separated with underscores (_)")
print("[3] Generate n-th fibonnaci number. How to use: fibonacci n")

command = input("Input command:")

start = time.time()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(bytes(command, "utf-8"))
    data = s.recv(1024)
end = time.time()

print('RESULT:\n{}'.format(data.decode("utf-8")))
print("Time elapsed:", end-start)
