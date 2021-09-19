
#!/usr/bin/python                                                                                                                                                                     

import socket
import _thread
from collections import defaultdict

active_sockets = []
zone_content = defaultdict(lambda: defaultdict(lambda: defaultdict))
# zone_content['z1'] = {100 : ['300,500','400,500']}
# zone_content['z1']['id_of_client'] = []

def on_new_client(clientsocket,addr):
    while True:
        msg = clientsocket.recv(1024)
        msg = msg.decode('utf-8').split(';') # 0 idx is function to call, 1 idx is zone number        
        
        if msg[0] == 'info':
            print(zone_content)
        
        #updateClient;zonename;id_of_client;x;y
        elif msg[0] == 'updateClient':
            locations = ''
            zone = msg[1]
            id_of_client = msg[2]
            zone_content[zone][id_of_client] = ';'.join(msg[slice(3,5)])
            temp_arr = []
            for key,value in zone_content.items():
                if key == zone:
                    for key2, value2 in value.items():
                        if key2 != id_of_client:
                            temp = key2 + ';' + value2
                            temp_arr.append(temp)
            if temp_arr == []:
                clientsocket.sendall('empty'.encode('utf-8'))
            else:
                print(';'.join(temp_arr).encode('utf-8'))
                clientsocket.sendall(';'.join(temp_arr).encode('utf-8'))
            

    clientsocket.close()

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP SOCKET
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # STREAM SOCKET
host = '127.0.0.1' # link to localhost
port = 65432 

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Quicker debugging because don't have to wait for socket to reset
# s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) # Something about forces the socket to write to the client immediately or something like that

s.bind((host, port))        
s.listen(5)             

print("Server active, accepting clients ...")

while True:
    c, addr = s.accept()
    if c and addr:
        _thread.start_new_thread(on_new_client,(c,addr))
        print ('Got connection from', addr)

s.close()