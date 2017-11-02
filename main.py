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


def regist_check(account):
	if baidu_check(account)==0:
		print("regist baidu!");
	else:
		print("not regist baidu")

if __name__ == '__main__':
	# account=raw_input(u'账号:')
	account="13164757102"
	regist_check(account)

