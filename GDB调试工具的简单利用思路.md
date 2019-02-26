## GDB调试工具的简单利用思路
------------------------------------------------
* 首先使用相应的编译器将源代码进行编译，比如c编写的test.c文件：  
`gcc gdbtest.c -g`  
这里加-g表示将源代码信息编译到可执行文件中。
* 然后开始调试，若不设置断点直接r就代表直接将程序运行到最后：
```
(gdb) r
Starting program: /root/文档/gdbtest 
n = 1, nGlobalVar = 88 /ntempFunction is called, a = 1, b = 2 /nn = 3[Inferior 1 (process 1958) exited normally]
```
* 使用指令b在main函数处设置断点：  
`(gdb) r main`
此时使用r将程序中断在main函数处（此时gdb显示的是断点的下一行代码），使用s执行下一行代码。
* 删除当前所有断点：d。
* 使用p n打印变量的值。
* 使用b x在第x行适合断点。
* 使用“c”命令继续（Continue）执行被调试程序（直到下一个断点）。
* 在调试时显示汇编代码：
`display /i $pc`
* q退出gdb。
-------------------------------------------------
#### 原文链接：
>https://blog.csdn.net/liigo/article/details/582231/
    