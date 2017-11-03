# -*- coding: utf-8 -*-

'''
Required
- requests (必须)
Info
- author : "caster"
- github : "https://github.com/Mycaster"
- date   : "2017.10.31"
'''

import sys  
reload(sys) 
sys.setdefaultencoding('utf8')
import baidu_check
from baidu_check import baidu_check

def result_output(ret, site):
	if ret == 1:
		print("already regist " + site)
	elif ret ==0:
		print("not regist " + site)
	else:
		print(site + " check failed!")

def regist_check(account):
	result_output(baidu_check(account), "baidu")
	# result_output(sina_check(account) , "sina")

if __name__ == '__main__':
	account=raw_input(u'账号:')
	# account="13164757102"
	regist_check(account)

