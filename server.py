import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREAD = 2
JOB_NUMBER = [1 , 2]
queue = Queue()
all_connection = []
all_address = []


# Create a Socket ( connect 2 computers )
def create_sockets():
    try:
        global host
        global port
        global s
        host = ''
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("There's a err happend: " + str(msg))

def binding_socket():
    try:
        global host
        global port
        global s
        print("Binding the port " + str(port))
        s.bind((host , port))
        s.listen(5)
    except socket.error as msg:
        print("Fail in binding the port " + str(msg) + "Retrying to connect...")
        binding_socket()

# Handling connections from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connection():
    for c in all_connection:
        c.close()

    del all_connection[:]
    del all_address[:]

    while True:
        try:
            conn , address = s.accept()
            s.setblocking(1) # prevent timeout
            all_connection.append(conn)
            all_address.append(address)
            print("Connection has been established "+ address[0])
        except:
            print("Connection err")

# 2nd Thead function 1,see all clients 2,select a client 3,Send commands to selected client
#
# def start_turtle():
#     cmd = input("turtle>")
#
#     if cmd == 'list':
#         list_connection()
#     elif 'select' in cmd:
#         conn = get_target(cmd)
#         if conn is not None:
#             send_target_commands(conn)
#     else:
#         print("Command is not recognised")

# Display all current active connections with the client

# def list_connection():
#     results = ''
#     selectedId = 0
#     for i,conn in enumerate(all_connection):
#         try:
#             conn.send(str.endcode(' '))
#             conn.recv(201480)
#         except:
#             del all_connection[i]
#             del all_address[i]
#             continue
#     result = str(i) + "  " + str(all_address[i][0] + '  ' + str(all_address[i][1] + "\n"))
#     print("----Client----" + "\n" + results)
#
# def get_target(cmd):
#     try:
#         target = cmd.replace('select ' ,'') # target = id
#         target = int(target)
#         conn = all_connection[target]
#         print("You care now connected to :" + str(all_address[target][0]))
#         print(str(all_address[target][0]) + ">" , end='')
#     except:
#         print("Selection is not valid")
#         return None
#
# def send_target_commands(conn):
#     while True:
#         try:
#             cmd = input()
#             if cmd == 'quit':
#                 break
#             if len(str.endcode(cmd) > 0):
#                 conn.send(str.endcode(cmd))
#                 client_response = str(conn.recv(20480) , 'utf-8')
#                 print(client_response , end='')
#         except:
#             print("Err command")