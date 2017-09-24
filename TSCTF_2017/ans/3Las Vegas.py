 # "exampleClient.py" is a simple client programed by Python.
# It can connect to the server, solve the question, and finally capture the flag.
# It's only a example. In the real test, you have to program it by yourself.
#-*- coding: utf-8 -*-

import socket
import time
import re
import math
timeout = 1000   
socket.setdefaulttimeout(timeout)
# 1 Socket Init
# 1.1 Set Host and Port
HOST = '10.105.42.5'
PORT = 43333

# 1.2 Connect to Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

for i in range (50):
    # 2 Receive the Message from Server
    # [sleep() before recv() is necessary]
    time.sleep(0.1)
    response = sock.recv(1024)
    response = response.decode('utf-8')   
    m = re.findall(r'(\w*[0-9]+)\w*',response)
    print(response)

    #ab
    a = int(m[1])
    b = int(m[2])
    c=a-(b+1)*(a//(b+1))
    # 3 Send the Answer to Server
    #c = c.encode('utf-8')
    while (a-c>0) :
        sock.send(str(c)+"\n")
        time.sleep(0.005)
        response = sock.recv(1024)
        response = response.decode('utf-8')
        print response        
        m = re.findall(r'(\w*[0-9]+)\w*',response)
        d=int(m[0])
        k=a-c-d
        c=b+1-k
        a=d
        
    sock.send(str(c)+"\n")
        

# 4 Receive the Flag from Server
time.sleep(0.01)
response = sock.recv(1024)
print (response)

# 5 Close the Socket
sock.close()


time.sleep(0.001)
