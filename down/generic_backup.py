# -*- coding:utf-8 -*-
import requests
import time
import re
import random
from bs4 import BeautifulSoup
from requests.exceptions import RequestException

'''
Example for parameters:
	base = 'http://m.banzhuer.org'
	postfix = '/8_8557/1367719.html'
	endpage = '/8_8557/'
'''

class DownloaderSignal:
	OK = 0
	REPEAT = 1


class ExtractionContent:
	def __init__(self, content, title, title_write_flag):
		self.content = content
		self.title = title
		self.title_write_flag = title_write_flag


class GenericDownloader:
	# constants
	_Headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	'cache-control': 'no-cache',
	'accept-encoding': 'gzip, deflate'}
	_Proxies = {'http': 'http://127.0.0.1:1087', 'https': 'https://127.0.0.1:1087'}
	
	def __init__(self, base, postfix, endpage, gbk=False, output='xiaoshuo.txt'):
		self._base = base
		self._postfix = postfix
		self._gbk = gbk
		self._output = output
		
		self._endpage = endpage

	def setpostfix(self, postfix):
		self._postfix = postfix
		
	def __fetch_data(self, hfile):
		url = self._base + self._postfix
		if url == self._endpage:
			print('Running to the endpage!!!')
			exit(0)
		print('--------------------------------------------------------')
		print(f'Fetching {url}')
		resp = requests.get(url, headers=self._Headers, proxies=self._Proxies)
		if self._gbk:
			bs = BeautifulSoup(resp.text.encode('iso-8859-1').decode('gbk', 'ignore'), 'lxml')
		else:
			bs = BeautifulSoup(resp.text, 'lxml')
		
		# extract the text
		signal, C = self.extraction(bs)
		if signal == DownloaderSignal.REPEAT: # something goes wrong, directly return the signal and bs
			return signal, bs

		# write title
		if C.title_write_flag:
			hfile.write(C.title + '\n\n')

		# replace all the unuseful text
		text = self.grep(C.text)
		
		# write to file
		hfile.write(text)
		hfile.write('\n')
		hfile.flush()
		
		return signal, bs
		
	def run(self):
		f = open(self._output, 'w', encoding='utf-8')
		while True:
			try:
				signal, bsobj = self.__fetch_data(f)
				if signal == DownloaderSignal.REPEAT:
					print('--------------------------------------------------------')
					print('Got REPEAT signal!!!')
					print('Waiting more time!!!')
					time.sleep(random.randint(5, 10))
					continue
			except RequestException as e:
				print('--------------------------------------------------------')
				print('RequestException ERROR!!!')
				print('Waiting more time!!!')
				print(e)
				time.sleep(random.randint(5,10))
				continue
			except Exception as e:
				print('--------------------------------------------------------')
				print('Other exception ERROR!!!')
				print(e)
				exit(1)

			if not self.next_page(bsobj):
				break
			w_tm = random.randint(5, 25) / 5
			print(f'Waiting for {w_tm} secs')
			time.sleep(w_tm)
	
	def extraction(self, bsobj):
		pass
	
	# optional, replace the text
	def grep(self, text):
		return text

	# 1. modify the self._postfix
	# 2. if end, return Flase, else return True
	def next_page(self, bsobj):
		pass