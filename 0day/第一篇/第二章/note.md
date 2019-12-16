# notes about chapter 2
## from 2.1
1. 每一个C++类成员都有一个this指针，在win中，这个指针一般使用ecx进行保存：
![测试](./this指针.JPG)

## 2.2.1 expriment
这里的auth标志位在buffer的下方：
>int authenticated;  
char buffer[8];// add local buffto be overflowed

利用思路：  
覆盖掉标志位。
这里的内存布局输入7777777如下:
```
buff[8]    71717171     qqqq
           00717171     NULLqqq
auth       00 00 00 01   真实存储为：   01 00 00 00 00
```
我们想要的:
```
buff[8]    71717171     qqqq
           00717171     NULLqqq
auth       00 00 00 00   真实存储为：   00 00 00 00 00
```
由于字符串末尾有NULL(00)作为结尾，所以我们输入8位的char型即可：
```
buff[8]     71717171       qqqq
            71717171       qqqq
auth        00000000       00 00 00 00
```
即我们想要得到的是00 00 00 00(这个为0，数值数据)，使用NULL将其覆盖即可。  
![success](./success.JPG)
## 2.3.2 experiment
首先查看我们想要的返回地址：
![retaddr](./ret_addr.JPG)
返回地址为：0x0040112F
使用Ultraedit进行修改覆盖地址的位置即可，从(8+4+4)=16的地方开始覆盖地址：
![com_addr](./comaddr.JPG)
运行即可：
![success2](./success2.JPG)

## 2.2.4 expriment

0x0019FB2C->0x31323334

user32.dll的基地址：

