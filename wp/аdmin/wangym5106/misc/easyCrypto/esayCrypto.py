import struct
import base64

cypher_text = 'DgYiZFttExBafXJPPn8BNhI9cwEhaUMgPmg+IA=='

flag = 'xxxxxxxxxxxxxxxxxxx'
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

	return base64.b64encode(cyphertext)


def decode(cipher64, iv):
	ciphertext = base64.b64decode(cipher64)
	cipher = struct.unpack("I" * (len(ciphertext) / 4), ciphertext)
	cipher = list(cipher)
	for i in range(len(cipher)-1,0,-1):
		cipher[i] = crypto(cipher[i]) ^ cipher[i-1]
	cipher[0] = crypto(cipher[0]) ^ iv
	raw = ''
	for c in cipher:
		raw += struct.pack("I", c)
	print raw

padding = 4 - len(flag) % 4
if padding != 0:
	flag = flag + "\x00" * padding

datas = struct.unpack("I" * (len(flag) / 4), flag)
result = encode(datas, iv)
print result

decode(cypher_text, iv)
