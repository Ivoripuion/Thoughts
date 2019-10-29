from pwn import *
context.log_level = 'debug'

p="./elf"
elf=ELF("./pivot")
libp=ELF("./pivot")

context.binary=p
io=process(p)

mov_rax_rax=0x0000000000400b05


payload=
io.sendline(payload)

io.interactive()
