import socket
import pickle

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command_args = data.decode("utf-8").split(" ")
            if command_args[0] == "sort":
                lst_arg = eval(command_args[1])
                lst_arg.sort()
                result = "Sorted list: " + str(lst_arg)
            conn.sendall(bytes(result, "utf-8"))