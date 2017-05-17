# "exampleClient.py" is a simple client programed by Python.
# It can connect to the server, solve the question, and finally capture the flag.
# It's only a example. In the real test, you have to program it by yourself.

import socket
import time

# 1 Socket Init
# 1.1 Set Host and Port
HOST, PORT = "127.0.0.1", int(2333)

# 1.2 Connect to Server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

# 2 Receive the Message from Server
# [sleep() before recv() is necessary]
time.sleep(0.1)
response = sock.recv(1024)
print response,

# 3 Send the Answer to Server
sendBuf = "42"
sock.send(sendBuf)
print sendBuf

# 4 Receive the Flag from Server
time.sleep(0.1)
response = sock.recv(1024)
print response

# 5 Close the Socket
sock.close()

time.sleep(10)
