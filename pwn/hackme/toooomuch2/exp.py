from pwn import *

p="./toooomuch"
context.binary=p
io=process(p)

payload=
io.sendline(payload)

io.interactive()
