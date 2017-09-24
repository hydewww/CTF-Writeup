#-*- coding: utf-8 -*-
import socket
import time
import re
import math
# 1 Socket Init
# 1.1 Set Host and Port
HOST = '10.105.42.5'
PORT = 41111
# 1.2 Connect to Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# 2 Receive the Message from Server
# [sleep() before recv() is necessary]
time.sleep(0.1)
response = sock.recv(1024)
response = response.decode('utf-8')
print (response)
# 正则表达式抓取数字
m = re.findall(r'(\w*[0-9]+)\w*',response)
a = int(m[2])
max = 0
while(a>0):
    if(max<a%10):
        max=a%10
    a//=10
# 3 Send the Answer to Server
sock.send(str(max)+"\n")

#由于第一次数是第2个，之后为第1个，故第一次单独执行，剩余49次循环

for i in range (49):
    time.sleep(0.1)
    response = sock.recv(1024)
    response = response.decode('utf-8')   
    m = re.findall(r'(\w*[0-9]+)\w*',response)
    print (response)
    a = int(m[1])
    print (a)
    max=0
    while(a>0):
        if(max<a%10):
            max=a%10
        a//=10
    sock.send(str(max)+"\n")

# 4 Receive the Flag from Server
time.sleep(0.01)
response = sock.recv(1024)
print (response)

# 5 Close the Socket
sock.close()
time.sleep(0.001)
