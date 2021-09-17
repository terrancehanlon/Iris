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
from collections import defaultdict

active_sockets = []
zone_content = defaultdict(lambda: defaultdict(lambda: defaultdict))
# zone_content['z1'] = {100 : ['300,500','400,500']}
# zone_content['z1']['id_of_client'] = []

def on_new_client(clientsocket,addr):
    # print(addr, " has connected");
    print("Creating new thread")
    while True:
        msg = clientsocket.recv(1024)
        # print(msg)
        msg = msg.decode('utf-8').split(';') # 0 idx is function to call, 1 idx is zone number
        # print(msg)
        # print(clientsocket)
        # if msg != '':
        #     print(msg)
        
        if msg[0] == 'info':
            print(zone_content)
        
        # #init;zonename
        # #return current list of ids and locations
        # if msg[0] == 'init':
        #     print("init getting locations")
        #     locations = ''
        #     for key,value in zone_content.items():
        #         # print(value)
        #         if key == msg[1]: #look for zone
        #             for key2, value2 in value.items():
        #                 print(value2)
        #                 locations = locations + (';'.join(value2))
        #                 locations = locations + ';'
        #     print(locations)
        #     if locations == '':
        #         clientsocket.sendall("empty".encode('utf-8'))
        #     else:
        #         clientsocket.sendall(locations.encode('utf-8'))                
        #     print('sent locations')

        # #updates the server with a clients location
        # #update;zonename;id_of_player;x;y
        # if msg[0] == 'updateServer':
        #     good = True
        #     msg.pop(0)
        #     for x in msg:
        #         if 'updateClient' in x:
        #             good = False
        #     # print(msg[2:])
        #     if good:
        #         if zone_content[msg[0]][msg[1]] != msg[2:]:
        #             zone_content[msg[0]][msg[1]] = msg[2:]
        #     clientsocket.sendall("recieved!".encode('utf-8'))

        #updates the client with other clients locations 
        #check for id on client?
        #updateClient;zonename;id_of_client;x;y
        elif msg[0] == 'updateClient':
            # print('updating client')
            locations = ''
            # print(msg)
            zone = msg[1]
            id_of_client = msg[2]
            #update clients location on server
            zone_content[zone][id_of_client] = ';'.join(msg[slice(3,5)])
            # print(zone_content)
            temp_arr = []
            for key,value in zone_content.items():
                if key == zone:
                    for key2, value2 in value.items():
                        # print(key2)
                        # print(value2)
                        if key2 != id_of_client:
                            temp = key2 + ';' + value2
                            temp_arr.append(temp)
                            # print(temp)
                            # print(temp_arr)
                            # locations = locations + (';'.join(value2))
            # locations = locations + ';'
            if temp_arr == []:
                # print('sending empty')
                clientsocket.sendall('empty'.encode('utf-8'))
            else:
                # print('locations not empty')
                # print(locations)
                # print(temp_arr)
                clientsocket.sendall(';'.join(temp_arr).encode('utf-8'))
            

    clientsocket.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a socket object
s = socket.socket()
host = '127.0.0.1' # Get local machine name
port = 65432                # Reserve a port for your service. 

print ('Server started!')
print ('Waiting for clients...')
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
    c, addr = s.accept()     # Establish connection with client.
    if c and addr:
        _thread.start_new_thread(on_new_client,(c,addr))
        print ('Got connection from', addr)
    # print(len(active_sockets))

s.close()