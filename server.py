# import socket

# HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
# PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.bind((HOST, PORT))
#     s.listen()
#     conn, addr = s.accept()
#     with conn:
#         print('Connected by', addr)
#         while True:
#             data = conn.recv(1024)
#             print(data.strip())
#             if not data:
#                 break
#             # conn.sendall(data)

#!/usr/bin/python           # This is server.py file                                                                                                                                                                           

import socket               # Import socket module
import _thread

active_sockets = []

def on_new_client(clientsocket,addr):
    # print(addr, " has connected");
    print("Creating new thread")
    while True:
        msg = clientsocket.recv(1024)
        msg = msg.decode('utf-8')
        print(type(msg))
        
        # msg = msg.join
        #do some checks and if msg == someWeirdSignal: break:
        print (addr, ' >> ', msg)
        # active_sockets.append(msg.split(","))
        clientsocket.sendall(str(len(msg)).encode('utf-8'))
    clientsocket.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a socket object
s = socket.socket()
host = '127.0.0.1' # Get local machine name
port = 65432                # Reserve a port for your service. 

print ('Server started!')
print ('Waiting for clients...')
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
    c, addr = s.accept()     # Establish connection with client.
    if c and addr:
        _thread.start_new_thread(on_new_client,(c,addr))
        print ('Got connection from', addr)
    # print(len(active_sockets))

s.close()