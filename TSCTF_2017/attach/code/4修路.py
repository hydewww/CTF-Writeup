#-*- coding: utf-8 -*-
import socket
import time
import re
id = []
sz = []
count = 800
for i in range (1001):
    id.append(i)
for i in range(1001):
    sz.append(1)
def union(p,  q):
    global count
    i = find(p)
    j = find(q)
    if (i == j):
        return 
    if (sz[i] < sz[j]):
        id[i] = j
        sz[j] += sz[i] 
    else:
        id[j] = i
        sz[i] += sz[j]
    count=count-1
def find(p):  
    while (p != id[p]):   
        id[p] = id[id[p]]
        p = id[p]
    return p
def connected(p, q):  
    return find(p) == find(q)
# 1 Socket Init
# 1.1 Set Host and Port
HOST = '10.105.42.5'
PORT = 44444

# 1.2 Connect to Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))
sock.send("\n")
# 2 Receive the Message from Server
# [sleep() before recv() is necessary]
time.sleep(0.1)
response = sock.recv(7*1024)
response = response.decode('utf-8')
m = re.findall(r'(\w*[0-9]+)\w*',response)

i=0

while(i<1600):
    union(  int(m[i]) ,   int(m[i+1])   )
    i+=2
print (response+"\n")
#asdfadsfasdfadsf
if(connected( int(m[1601]) , int(m[1602]))  ):
    sock.send("yes\n")
else:
    sock.send("no\n")

# 3 Send the Answer to Server
for i in range (9999):
    time.sleep(0.005)
    response = sock.recv(1024)
    response = response.decode('utf-8')
    m = re.findall(r'(\w*[0-9]+)\w*',response)
    print(response)
    if(connected( int(m[1]) , int(m[2]))  ):
        sock.send("yes\n")
    else:
        sock.send("no\n")
#print (sendBuf)

# 4 Receive the Flag from Server
time.sleep(0.1)
response = sock.recv(1024)
print (response)

# 5 Close the Socket
sock.close()
time.sleep(10)
