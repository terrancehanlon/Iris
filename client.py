#!/usr/bin/env python3


import socket

HOST = '127.0.0.1'   # The server's hostname or IP address
print(HOST)
PORT = 65432        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        # m = input("enter message: ")
        s.sendall("info;".encode('utf-8'))
        data = s.recv(1024)
        # print('Received', repr(data))
