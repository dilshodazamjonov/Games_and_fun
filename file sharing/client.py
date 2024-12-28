import socket
import threading
from base64 import encode

from pyexpat.errors import messages


def recieve_file(conn):
    file = conn.recv(1024).decode()
    print(f'received filename: {file}')
    with open(file, mode='w') as f:
        data = conn.recv(1024).decode()
        f.write(data)
    print(f'Received successfully!\n New filename is: {file}')

def send_file(conn):
    filename = input('Enter the filename you would like to send: ')
    try:
        fi = open(filename, 'r')
        data = fi.read()
        if not data:
            print('No data in file')
        else:
            conn.send('filename'.encode())
            conn.send(filename.encode())
            print('filename successfully received from client\n Sending file data... ')
            while data:
                conn.send(str(data).encode())
                data = fi.read()
            fi.close()
    except IOError:
        print('You entered an invalid filename\n Please enter the valid file name: ')

def recieve(conn, stop):
    while not stop.is_set():
        data = conn.recv(1024).decode()
        if str(data) == 'filename':
            recieve_file(conn)
        elif str(data) == 'bye':
            conn.send('later gator!'.encode())
            stop.set()
            break
        else:
            print(f'from server: {str(data)}')


def send(conn, stop):
    message = ''
    while message.lower().strip() != 'bye':
        message = input(' --> ')
        if message.lower().strip() == 'send file':
            send_file(conn)
            message = ''
            continue
        conn.send(message.encode())
    stop.set()

def server_program():
    host = socket.gethostname()
    port = 5432

    server_socket = socket.socket()
    server_socket.bind((host,port))

    server_socket.listen(2)
    conn, address = server_socket.accept()
    print(f'Connection from: {str(address)}')

    stop_event = threading.Event()
    send_thread = threading.Thread(target=send, args=(conn, stop_event,))
    receive_thread = threading.Thread(target=recieve, args=(conn, stop_event,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

    conn.close()

if __name__ == '__main__':
    server_program()

