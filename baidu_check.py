# -*- coding: utf-8 -*-
import random
import rsa
import binascii
import requests
import time
import math
import hashlib
from base64 import b64decode

# agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
headers={
	'user-agent': agent,
    "Host": "passport.baidu.com",
}
session = requests.session()



def hex_md5(str):
	return hashlib.md5(str).hexdigest()

def get_gid():
	random_str=""
	for s in "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx":
		t = int(16*random.random()) | 0
		if s=="x":
			s = hex(t)[2:]
		elif s=="y":
			s = (3 & t | 8)
			s = hex(s)[2:]
		random_str=random_str+s
	return random_str.upper()

def get_callback():
    loopabc = '0123456789abcdefghijklmnopqrstuvwxyz'
    prefix = "bd__cbs__"
    n = math.floor(random.random() * 2147483648)
    a = []
    while n != 0:
        a.append(loopabc[int(n % 36)])
        n = n // 36
    a.reverse()
    callback = prefix + ''.join(a)
    return callback

def get_token():
	global cookies
	token_callback = get_callback()
	#不能使用 params, 会自动排序参数,百度对参数的提交顺序有要求
	token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt="
	token_url = token_url + str(int(time.time()*1000)) + "&class=regPhone&gid="
	token_url = token_url + gid + "&app=&traceid=&callback="
	token_url = token_url + token_callback

	rsp = session.get(token_url, headers=headers , cookies=cookies)
	cookies = rsp.cookies
	try :
		token_content = rsp.content.replace(token_callback, "")
		return eval(token_content)['data']['token']
	except Exception as e:
		print(e)
		print("response: "+rsp.content)
		return ""

def get_moonshad(account):
	n = hex_md5(account+"Moonshadow")
	#最多替换一次
	n = n.replace("o", "ow", 1).replace("d", "do" ,1).replace("a", "ad" ,1)
	n = n.replace("h", "ha" ,1).replace("s", "sh", 1).replace("n", "ns" ,1).replace("m", "mo" ,1)
	return n

def get_cookies():
	#token 的获取必须带上cookies, 不然总是报错 "token":"the fisrt two args should be string type:0,1!"
	home_url = "https://www.baidu.com"
	rsp = session.get(home_url, headers=headers)
	return rsp.cookies


cookies=get_cookies()
gid=get_gid()
token=get_token()

def baidu_check(account):
	if token == "":
		print("get_token null!!")
		return -1
	# print(token)
	callback = get_callback()
	moonshad = get_moonshad(account)
	timenow = str(int(time.time()*1000))

	regist_url = "https://passport.baidu.com/v2/?regphonecheck&token="
	regist_url = regist_url + token +"&tpl=mn&apiver=v3&tt="
	regist_url = regist_url + timenow + "&phone="
	regist_url = regist_url + account + "&moonshad="
	regist_url = regist_url + moonshad + "&countrycode=&gid="
	regist_url = regist_url + gid + "&exchange=0&isexchangeable=1&action=reg&traceid=&callback="
	regist_url = regist_url + callback

	# print(regist_url)
	rsp = session.get(regist_url, headers=headers, cookies=cookies)
	rsp = rsp.content.replace(callback, "")
	rsp_json = eval(rsp)
	try :
		errno = rsp_json['errInfo']['no']
		if errno=="0":	#未注册
			return 0
		elif errno=="130020":  #已注册
			return 1
	except Exception as e:
		print(rsp_json)
		print(e)
	return -1


