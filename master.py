import socket
import pickle

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'sort [5,7,4,3,9,10]')
    data = s.recv(1024)

print('Received', data.decode("utf-8"))