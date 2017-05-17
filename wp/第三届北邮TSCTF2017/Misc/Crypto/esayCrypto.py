import struct
import base64
import os

cypher_text = 'DgYiZFttExBafXJPPn8BNhI9cwEhaUMgPmg+IA=='

#flag = 'TSCTF{    }'
flag='DgYiZFttExBafXJPPn8BNhI9cwEhaUMgPmg+IA=='
flag2='DgYiZFttExBafXJPPn8BNhI9cwEhaUMgPmg+IA=='
iv = struct.unpack("I", 'x1a0')[0]
print 'iv is ', hex(iv)


def crypto(data):
	return data ^ data >> 16

def encode(datas, iv):
	cypher = []
	datas_length = len(datas)
	cypher += [crypto(datas[0] ^ iv)]

	for i in range(1, datas_length):
		cypher += [crypto(cypher[i-1] ^ datas[i])]

	cyphertext = ''
	for c in cypher:
		cyphertext += struct.pack("I", c)
		print 'cyphertext = ',cyphertext

	print 'cyphertext is',cypher

	return base64.b64encode(cyphertext)

def recode(datas, iv):
        cypher = []
        datas_length = len(datas)
        cypher += [crypto(datas[0]) ^ iv]
        for i in range(1, datas_length):
                cypher += [crypto(datas[i]) ^ datas[i-1]]

        print 'd= ', cypher
        #e = struct.pack("I"*
        cyphertext = ''
        for c in cypher:
                cyphertext += struct.pack("I", c)
        print 'e=',cyphertext
        return base64.b64encode(cyphertext)


padding = 4 - len(flag) % 4
if padding != 0:
	flag = flag + "\x00" * padding

datas = struct.unpack("I" * (len(flag) / 4), flag)
print 'datas is ', datas
#a= encode(datas, iv)
a= flag
print 'a= ', a
b= base64.b64decode(a)
print 'b= ',b
c= struct.unpack("I" * (len(b) / 4), b)
print 'c= ',c
print recode(c,iv)
padding2 = 4 - len(flag2) % 4
if padding2 != 0:
	flag2 = flag2 + "\x00" * padding2

datas2 = struct.unpack("I" * (len(flag2) / 4), flag2)
print 'datas2 is',datas2
print recode(datas2,iv)
os.system('pause')

