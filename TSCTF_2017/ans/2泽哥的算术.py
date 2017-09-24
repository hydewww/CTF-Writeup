#-*- coding: utf-8 -*-
import socket
import time
import re
import math
# 1 Socket Init
# 1.1 Set Host and Port
HOST = '10.105.42.5'
PORT = 42222
# 1.2 Connect to Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

for i in range (50):
    # 2 Receive the Message from Server
    # [sleep() before recv() is necessary]
    time.sleep(0.1)
    response = sock.recv(1024)
    response = response.decode('utf-8')   
    print (response)
    # 正则表达式，抓下数字
    m = re.findall(r'(\w*[0-9]+)\w*',response)
    # 
    a = int(m[1])
    b = int(m[2])
    ans = 1
    while(b>0):
        if(b%2==1):
            c=c*a%10000
        b//=2
        a=a*a%10000

    # 3 Send the Answer to Server
    sock.send(str(ans)+"\n")

# 4 Receive the Flag from Server
time.sleep(0.01)
response = sock.recv(1024)
print (response)
# 5 Close the Socket
sock.close()
time.sleep(0.001)
