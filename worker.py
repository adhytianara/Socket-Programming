import socket
import requests

HOST = ''           # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

while True:
    conn, addr = s.accept()
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
        elif command_args[0] == "book_search":
            book_arg = command_args[1].split("\"")[1]
            r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + book_arg.replace("_", "%20"))
            r_json = r.json()
            result = "Buku ditemukan: {}\n".format(r_json["totalItems"])

            limit = 15
            if len(r_json["items"]) < 15:
                limit = len(r_json["items"])
            for i in range(0,limit):
                info_buku = r_json["items"][i]["volumeInfo"]
                result += "[{}] {}\n".format(i+1, info_buku["title"])
        elif command_args[0] == "fibonacci":
            fib_num = eval(command_args[1])

            def fibonacci(n):
                if n <= 1:
                    return n
                return fibonacci(n-1) + fibonacci(n-2)
                
            
            result = "Fibonacci ke-{}: {}".format(fib_num, fibonacci(fib_num))
        conn.sendall(bytes(result, "utf-8"))
