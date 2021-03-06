import socket
import requests
import time
from _thread import *

HOST = '127.0.0.1'           # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def main():
    status = {"status": 'ACTIVE'}
    status_job = {"status_job":'DO NOTHING'}
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    while True:
        print("Waiting for new connection")
        client, addr = server.accept()
        client.sendall(bytes('Connection accepted', "utf-8"))
        print('Connected by', addr)

        data = client.recv(1024).decode('utf-8')
        if data == "CHECK_AVAILABILITY":
            start_new_thread(check_availability, (client, addr, status))
        elif data == "CHECK_STATUS_JOB":
            start_new_thread(check_status_job, (client, addr, status_job))
        elif data == "EXECUTE_JOB":
            status['status'] = "BUSY"
            status_job['status_job'] = "RUNNING"
            job = client.recv(1024).decode('utf-8')
            start_new_thread(execute_job, (client, job, status, status_job))


def check_availability(client, addr, status):
    client.sendall(bytes(status.get('status'), 'utf-8'))
    client.close()

def check_status_job(client, addr, status_job):
    client.sendall(bytes(status_job.get('status_job'), 'utf-8'))
    client.close()

def execute_job(client, job, status, status_job):
    try:
        job_args = job.split(" ")
        start = time.time()

        result = "Unknown job, try again"
        if job_args[0] == "sort":
            result = sort_job(job_args[1])
        elif job_args[0] == "book_search":
            result = book_search_job(job_args[1])
        elif job_args[0] == "fibonacci":
            fib_num = eval(job_args[1])
            result = "Fibonacci ke-{}: {}".format(fib_num, fibonacci_job(fib_num))
        
        end = time.time()
        print(f'result {result}')
        status_job['status_job'] = "FINISHED"
        client.sendall(bytes(f'{result}\nTime elapsed: {end-start}', "utf-8"))
        status['status'] = 'ACTIVE'
        client.close()
    except(IndexError):
        client.sendall(bytes('Unknown job, try again', "utf-8"))
        status['status'] = 'ACTIVE'

def sort_job(arr):
    lst_arg = eval(arr)
    lst_arg.sort()
    sorted_arr = "Sorted list: " + str(lst_arg)
    return sorted_arr


def book_search_job(title):
    book_arg = title.split("\"")[1]
    r = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + book_arg.replace("_", "%20"))
    r_json = r.json()
    result = "Buku ditemukan: {}\n".format(r_json["totalItems"])

    limit = 15
    if len(r_json["items"]) < 15:
        limit = len(r_json["items"])
    for i in range(0,limit):
        info_buku = r_json["items"][i]["volumeInfo"]
        result += "[{}] {}\n".format(i+1, info_buku["title"])
    return result


def fibonacci_job(n):
    if n <= 1:
        return n
    return fibonacci_job(n-1) + fibonacci_job(n-2)
    

if __name__ == '__main__':
    main()
