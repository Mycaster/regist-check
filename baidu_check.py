# -*- coding: utf-8 -*-
import random
import rsa
import binascii
import requests
import time
import math
from base64 import b64decode

# agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36"
headers={
	'user-agent': agent,
    "Host": "passport.baidu.com",
}
session = requests.session()



def hex_md5(str):
	import hashlib
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
	token_callback = get_callback()
	#不能使用 params, 会自动排序参数,百度对参数的提交顺序有要求
	token_url = "https://passport.baidu.com/v2/api/?getapi&tpl=mn&apiver=v3&tt="
	token_url = token_url + str(int(time.time()*1000)) + "&class=regPhone&gid="
	token_url = token_url + gid + "&app=&traceid=&callback="
	token_url = token_url + token_callback

	rsp = session.get(token_url, headers=headers , cookies=cookies)
	token_content = rsp.content.replace(token_callback, "")
	token_content = eval(token_content)
	return token_content['data']['token']

def get_moonshad(account):
	n = hex_md5(account+"Moonshadow")
	n = n.replace("o", "ow").replace("d", "do").replace("a", "ad")
	n = n.replace("h", "ha").replace("s", "sh").replace("n", "ns").replace("m", "mo")
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
	print(token)
	regist_url = "https://passport.baidu.com/v2/?regphonecheck&token="
	regist_url = regist_url + token +"&tpl=mn&apiver=v3&tt="
	regist_url = regist_url + str(int(time.time()*1000)) + "&phone="
	regist_url = regist_url + account + "&moonshad="
	regist_url = regist_url + get_moonshad(account) + "&countrycode=&gid="
	regist_url = regist_url + gid + "&exchange=0&isexchangeable=1&action=reg&traceid=&callback="
	regist_url = regist_url + get_callback()

	rsp = session.get(regist_url, headers=headers)
	print(rsp.content)


