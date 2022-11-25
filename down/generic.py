# -*- coding:utf-8 -*-
import requests
import time
import unicodedata
import html
import re
import random
import urllib3
from bs4 import BeautifulSoup
from collections import namedtuple
import sys

sys.setrecursionlimit(100000)

'''
Example for parameters:
	base = 'http://m.banzhuer.org'
	postfix = '/8_8557/1367719.html'
	endpage = '/8_8557/'
'''

urllib3.disable_warnings()

Contents = namedtuple('Contents', 'text title title_write_flag')
def normalize_html_text(text):
	text = html.unescape(text)
	text = unicodedata.normalize('NFKD', text)
	return text

class GenericDownloader:
	# constants
	_Headers = {
	'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
	'cache-control': 'no-cache',
	'accept-encoding': 'gzip, deflate'}
	_Proxies = {'http': 'http://127.0.0.1:7890'}
	
	def __init__(self, base, postfix, end_page=None, gbk=False, output='xiaoshuo.txt', reconnections_limit=100, verbose=True):
		"""
		Generic downloader, must reimplement next_page() and extraction() methods.

		:param base: str, static part for url, like 'https://xx.xx.com', notice that this str should not be ended with '/'
		:param postfix: str, variational part for url, like '/xx/xx.html', notice that this str should be started with '/'
		:param endpage: str, full url for termination, if set to None, returning False in next_page() method to denote
		:param gbk: bool, use gbk or not
		:param output: str
		:param reconnections_limit: int, maximum number for reconnection times
		:param verbose: bool, show more information
		"""
		self._base = base
		self._postfix = postfix
		self._url = None
		self.set_postfix(postfix)
		self._gbk = gbk
		self._output = output
		self._end_page = end_page
		self._verbose = verbose

		self._reconnections_limit = reconnections_limit
		self._reconnection_counter = 0

		self._episode_time = 5
		self._max_episode = 20
		self._episode_counter = 0

	def _random_wait(self, success):
		if success:
			self._episode_counter = 0
		self._episode_counter += 1
		if self._episode_counter > self._max_episode:
			self._episode_counter = self._max_episode
		max_time = self._episode_counter * self._episode_time
		rndtm = random.randint(max_time-self._episode_time, max_time)
		if self._verbose:
			print(f'Random waiting for {rndtm} sec')
		time.sleep(rndtm)

	def set_postfix(self, postfix):
		self._postfix = postfix
		self._url = self._base + self._postfix

	def set_full_url(self, full_url):
		self._url = full_url
		self._base, self._postfix = re.findall(r'(.+\.[a-z]+)(/.+)', full_url)[0]

	def _parse_and_write(self, hfile):
		print(f'Fetching {self._url}')
		resp = requests.get(self._url, headers=self._Headers, proxies=self._Proxies, verify=False)
		if self._gbk:
			bs = BeautifulSoup(resp.text.encode('iso-8859-1').decode('gbk', 'ignore'), 'lxml')
		else:
			bs = BeautifulSoup(resp.text, 'lxml')
		C = self.parse(bs)

		# write title and text
		if C.title_write_flag:
			if self._verbose:
				print(f'Write chapter title with {C.title}')
			hfile.write(C.title + '\n\n')
		text = normalize_html_text(C.text)
		hfile.write(text+'\n\n')
		hfile.flush()
		return bs

	def run(self):
		f = open(self._output, 'w', encoding='utf-8')
		while True:
			try:
				bsobj = self._parse_and_write(f)
				self._reconnection_counter = 0
				self._random_wait(True)
				if self._verbose:
					print('----------------------------------over----------------------------------')
			except Exception as e:
				print('Exception occurred!!!')
				print(e)
				self._random_wait(False)
				self._reconnection_counter += 1
				print(f'Reconnection counter {self._reconnection_counter}')
				if self._reconnection_counter >= self._reconnections_limit:
					print('Max reconnections exceed, exit!!!')
					print(f'Error url {self._url}')
					exit(1)

			next_page_end = not self.next_page(bsobj)
			if next_page_end or (self._end_page and self._url == self._end_page):
				break

		f.close()
		print('finished!')

	# two methods must be overridden
	def parse(self, bsobj):
		"""
		Parse beautifulsoup object to get text and title
		:param bsobj: BS4 object
		:return: Contents(text, title, title_write_flag)
		"""
		return Contents('', '', False)

	def next_page(self, bsobj):
		"""
		Turn to next page with set_postfix() and set_full_url() methods
		:param bsobj: BS4 object
		:return: bool, True means next page set okay, False means this whole activity is done (if end_page is set, this method can leave it behind)
		"""
		return True