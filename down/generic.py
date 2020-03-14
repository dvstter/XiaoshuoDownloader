# -*- coding:utf-8 -*-
import requests
import time
import re
import random
from bs4 import BeautifulSoup

"""
Example for parameters:
	base = "http://m.banzhuer.org"
	postfix = "/8_8557/1367719.html"
	endpage = "/8_8557/"
"""
class GenericDownloader:
	# constants
	_Headers = {
	"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
	"cache-control": "no-cache",
	"accept-encoding": "gzip, deflate"}
	_Proxies = {"http": "http://127.0.0.1:1087", "https": "https://127.0.0.1:1087"}
	
	def __init__(self, base, postfix, gbk=False, endpage=None, output="xiaoshuo.txt"):
		self._base = base
		self._postfix = postfix
		self._gbk = gbk
		self._output = output
		
		if endpage:
			self._endpage = endpage
		else:
			self.endpage = "/{}/".format(self._postfix.split("/")[1])
		
	def setpostfix(self, postfix):
		self._postfix = postfix
		
	def __generic_grep(self, text):
		text = re.sub(r"&[a-z;]+", "", text)
		return re.sub(r"<[a-z]+?>", "", text)
	
	def __fetch_data(self, hfile):
		url = self._base + self._postfix
		print("--------------------------------------------------------")
		print(f"Fetching {url}")
		resp = requests.get(url, headers=self._Headers, proxies=self._Proxies)
		if self._gbk:
			bs = BeautifulSoup(resp.text.encode("iso-8859-1").decode('gbk', "ignore"), "lxml")
		else:
			bs = BeautifulSoup(resp.text, "lxml")
		
		# extract the text
		text = self.extraction(bs)
		
		# replace all the unuseful text
		text = self.__generic_grep(text)
		text = self.grep(text)
		
		# write to file
		hfile.write(text)
		hfile.write("\n")
		hfile.flush()
		
		return bs
		
	def run(self):
		f = open(self._output, "w", encoding="utf-8")
		while True:
			try:
				bsobj = self.__fetch_data(f)
			except Exception as e:
				print("--------------------------------------------------------")
				print("ERROR!!!")
				print("Waiting more time!!!")
				time.sleep(random.randint(5,10))
				continue
				
			if not self.next_page(bsobj):
				break
			w_tm = random.randint(5, 25) / 5
			print(f"Waiting for {w_tm} secs")
			time.sleep(w_tm)
	
	# 1. use bsobj extract the data
	# 2. return text result
	def extraction(self, bsobj):
		pass
	
	# optional, replace the text
	def grep(self, text):
		return text
		
	# 1. modify the self._postfix
	# 2. if end, return Flase, else return True
	def next_page(self, bsobj):
		pass