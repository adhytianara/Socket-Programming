import socket
import time
import random
from _thread import *

workers = {
    "127.0.0.1" : "Unknown status",
    "127.0.0.2" : "Unknown status"
}
PORT = 65432        # The port used by the server
states = ""

def main():
    print("\nChecking the initial status of the workers")
    check_worker_availability()
    while True:
        user_action = print_list_of_actions()
        if user_action == 1:
            job = print_list_of_jobs()
            start_new_thread(execute_jobs, (job,))
        elif user_action == 2:
            start_new_thread(check_worker_availability, ())
        elif user_action == 0:
            print('Exit progam')
            exit()



def execute_jobs(job):
    available_worker = []

    for worker, status in workers.items():
        if status == "ACTIVE":
            available_worker.append(worker)
            break
    else:
        print('\nNo available worker found')
        return

    random_number_balancer = random.randint(0, len(available_worker)-1) 
    selected_worker = available_worker[random_number_balancer]
    workers[selected_worker] = "BUSY"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((selected_worker, PORT))

    # Print Worker 'IP': Connection accepted
    data = client.recv(1024).decode('utf-8')
    print(f'\nWorker {worker}: {data}')

    client.sendall(bytes("EXECUTE_JOB", "utf-8"))
    client.sendall(bytes(job, "utf-8"))

    result = client.recv(1024).decode('utf-8')
    print_job_result(result, job)
    workers[worker] = 'ACTIVE'



def check_worker_availability():
    for worker, status in workers.items():
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((worker, PORT))

            # Print Worker 'IP': Connection accepted
            data = client.recv(1024).decode('utf-8')
            print(f'\nWorker {worker}: {data}')

            # Print Worker 'IP': 'Status'
            client.send(bytes('CHECK_AVAILABILITY','utf-8'))
            data = client.recv(1024).decode('utf-8')
            workers[worker] = data
            print(f'Worker {worker}: {data}')

        except(OSError):
            print(f"Worker {worker}: DEAD")
            workers[worker] = 'DEAD'
            continue



def print_list_of_actions():
    states = "Action"
    action = input('\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
        '-------------------- WAITING FOR NEW ACTIONS --------------------',
        '*** List of actions: ***',
        "[1] Execute jobs on server",
        "[2] Check worker node availability",
        "[0] Exit",
        '************************',
        "Input Action(just number): "))
    return int(action)



def print_list_of_jobs():
    states = "Job"
    # print('\n-------------------- Waiting for new jobs --------------------')
    job = input('\n{}\n{}\n{}\n{}\n{}\n{}'.format(
        "*** List of jobs: ***",
        "[1] List sorting. \nHOW TO USE: sort [list]",
        "[2] Book search. \nHOW TO USE: book_search \"Harry_potter\". \nNote: book title in quotes and separated with underscores (_)",
        "[3] Generate n-th fibonnaci number. \nHOW TO USE: fibonacci n",
        '*********************',
        "Input Job(pay attention to 'HOW TO USE'): "
    ))
    return job



def print_job_result(result, job):
    print('\n\n{}\n{}\n{}\n{}\n{}\n\n'.format(
        '-------------------------------------------- RESULT --------------------------------------------',
        f'RESULT FROM PREVIOUS "{job}" JOB',
        f'{result}',
        '***  To continue using the program, follow the instructions before this result section  ***',
        '------------------------------------------ END RESULT ------------------------------------------'))
    print(states)

if __name__ == '__main__':
    main()