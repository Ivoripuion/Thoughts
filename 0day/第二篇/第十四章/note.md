# notes about chapter 14

## from 14.1

开启SEHOP：

手工在注册表中HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session
Manager\kernel找到DisableExceptionChainValidation项，将该值设置为0，即可启用SEHOP。

### SEHOP的原理

对SEH链进行检查，检查链表的最后一项是否为系统固定的终极异常处理函数，若是则表明SEH链完整，否则就有可能发生SEH覆盖攻击。


验证代码：

```C++
if (process_flags & 0x40 == 0) {   //如果没有 SEH 记录则不进行检测
    if (record != 0xFFFFFFFF) {        //开始检测 
        do {

            if (record < stack_bottom || record > stack_top)// SEH 记录必须位于栈中
                goto corruption;

            if ((char*)record + sizeof(EXCEPTION_REGISTRATION) > stack_top)
            //SEH 记录结构需完全在栈中
                goto corruption;

            if ((record & 3) != 0)       //SEH 记录必须 4 字节对齐
                goto corruption;

            handler = record->handler;

            if (handler >= stack_bottom && handler < stack_top)
            //异常处理函数地址不能位于栈中 
                goto corruption;
            
            record = record->next;

        }while (record != 0xFFFFFFFF);   //遍历 S.E.H 链

        if ((TEB->word_at_offset_0xFCA & 0x200) != 0) {

            if (handler != &FinalExceptionHandler)
                goto corruption;

        }
    }
}
```

书中介绍了三种攻击方法：

（1）不去攻击 S.E.H，而是攻击函数返回地址或者虚函数等。

（2）利用未启用 SEHOP 的模块。

（3）伪造 S.E.H 链。


## from 14.5 伪造 S.E.H 链表


前提：系统的ASLR不能启用

纯理论，在实际生产中，DEP以及ASLR均开启的情况下很难成功。

参考：https://bbs.pediy.com/thread-104707.htm