# note about chapter 8
## from 8.1 format string
测试程序的堆栈情况：

![f_s1](./f_s1.JPG)

此时首先入栈的格式化字符串读取前面进入栈的两个数：44（0x2C），77（0x4D）。但是第二个格式化字符串参数没有数据列表，于是顺着栈往下读，就是4218928（0x00406030）以及44（0x2C），若是继续读取就是77（0x4D）。

![f_s2](./f_s2.JPG)

常见的格式化字符串漏洞：
```
int printf( const char* format [, argument]... );
int wprintf( const wchar_t* format [, argument]... );
int fprintf( FILE* stream, const char* format [, argument ]...);
int fwprintf( FILE* stream, const wchar_t* format [, argument ]...);
int sprintf( char *buffer, const char *format [, argument] ... );
int swprintf( wchar_t *buffer, const wchar_t *format
[, argument] ... );
int vprintf( const char *format, va_list argptr );
int vwprintf( const wchar_t *format, va_list argptr );
int vfprintf( FILE *stream, const char *format, va_list argptr );
int vfwprintf( FILE *stream, const wchar_t *format, va_list argptr );
int vsprintf( char *buffer, const char *format, va_list argptr );
int vswprintf( wchar_t *buffer, const wchar_t *format, va_list argptr );
```

## from 8.2 injection
[见这里](https://github.com/Ivoripuion/Thoughts/blob/master/web/sqlInjec_note.md)

第七章的windows mobile早就被淘汰了。这一章的大部分都是些web相关的，曾经都已经学习大致。
