from zlib import crc32
from itertools import permutations
from string import printable
from multiprocessing import Pool


R = []
for i in range(0x100):
	R.append(bytes([i]))

HASHES = [
	0x664bf424,
	0x1f43ca81,
	0x6d06cca3
]

PROC = 8

def gs(n: int):
	for k in range(0x100//PROC*n, min(0x100//PROC*(n+1), 0x100)):
		c = bytes([k])
		print('started', repr(c))
		for key in permutations(R, 3):
			s = c + b''.join(key)
			h = crc32(s)
			if h in HASHES:
				print(repr(s), hex(h))

if __name__ == '__main__':
	with Pool(PROC) as p:
		p.map(gs, range(PROC))

# result:
# b'C3Cd' 0x1f43ca81
# b'Ea4Y' 0x6d06cca3
# b'EcRy' 0x664bf424