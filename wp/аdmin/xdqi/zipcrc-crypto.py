# -*- coding: utf-8 -*-  
import random, base64  
from hashlib import sha1  

key = 'TSCTF2017'

ctMessage = 'k6QqE3TU2qfqytHIatHD6DUOT+7D6vPXFUofQyF7dXjPhkPX9OnN/W5OxkvMfa0='
rawMessage = b'\x93\xa4*\x13t\xd4\xda\xa7\xea\xca\xd1\xc8j\xd1\xc3\xe85\x0eO\xee\xc3\xea\xf3\xd7\x15J\x1fC!{ux\xcf\x86C\xd7\xf4\xe9\xcd\xfdnN\xc6K\xcc}\xad'

def crypt(data, key):  
    x = 0  
    flow = list(range(256))
    for i in range(256):  
        x = (x + flow[i] + ord(key[i % len(key)])) % 256  
        flow[i], flow[x] = flow[x], flow[i]  
    x = y = 0  
    out = []  
    for char in data:  
        x = (x + 1) % 256  
        y = (y + flow[x]) % 256  
        flow[x], flow[y] = flow[y], flow[x]  
        out.append(chr(ord(char) ^ flow[(flow[x] + flow[y]) % 256]))  
  
    return b''.join(out)  
  
def tsencode(data, key=key, encode=base64.b64encode, salt_length=16):  
    salt = b''  
    for n in range(salt_length):  
        salt += chr(random.randrange(256))  
    data = salt + crypt(data, sha1(key + salt).digest())  
    if encode:  
        data = encode(data)  
    return data  

def decrypt(data, key):
    x = 0  
    flow = list(range(256))
    for i in range(256):  
        x = (x + flow[i] + ord(key[i % len(key)])) % 256  
        flow[i], flow[x] = flow[x], flow[i]
    x = y = 0  
    out = []  
    for char in data:  
        x = (x + 1) % 256  
        y = (y + flow[x]) % 256  
        flow[x], flow[y] = flow[y], flow[x]

    for char in data[::-1]:
        out.insert(0, chr(ord(char) ^ flow[(flow[x] + flow[y]) % 256]))
        flow[x], flow[y] = flow[y], flow[x]
        y = (y - flow[x]) % 256  
        x = (x - 1) % 256

    print(''.join(out))
    print(ctMessage)
    print(tsencode(out, key))


def tsdecode():
    salt = rawMessage[:16]
    ciphertext = rawMessage[16:]  # data front, digest end 20
    decrypt(ciphertext, sha1(key + salt).digest())

if __name__ == '__main__':
    tsdecode()
  
