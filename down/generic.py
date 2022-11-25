# -*- coding:utf-8 -*-
import multiprocessing
import requests
import time
import unicodedata
import html
import re
import queue
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

		self._parse_contents_waiting_time = 8

		self._reconnections_limit = reconnections_limit
		self._reconnection_counter = 0

		self._episode_time = 5
		self._max_episode = 20
		self._episode_counter = 0

	def _random_wait(self, success):
		"""
		Wait for one random integer seconds.

		:param success: bool, last execution success or not
		:return: None
		"""
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

	@staticmethod
	def write_contents(hfile, contents):
		if contents.title_write_flag:
			hfile.write(contents.title + '\n\n')
		text = normalize_html_text(contents.text)
		hfile.write(text+'\n\n')
		hfile.flush()

	@staticmethod
	def parse_text_and_next_postfix(safe_queue, url, filename, headers, proxies, gbk, parse_func, next_page_func, verbose):
		print(f'Fetching {url}')
		resp = requests.get(url, headers=headers, proxies=proxies, verify=False)
		if gbk:
			bs = BeautifulSoup(resp.text.encode('iso-8859-1').decode('gbk', 'ignore'), 'lxml')
		else:
			bs = BeautifulSoup(resp.text, 'lxml')
		contents = parse_func(bs)
		next_page_continue, postfix = next_page_func(bs)
		safe_queue.put((contents, next_page_continue, postfix))

	def run(self):
		hfile = open(self._output, 'w', encoding='utf-8')
		while True:
			try:
				safe_queue = multiprocessing.Queue()
				proc = multiprocessing.Process(target=self.parse_text_and_next_postfix, args=(safe_queue, self._url, self._output, self._Headers, self._Proxies, self._gbk, self.parse, self.next_page, self._verbose))
				proc.start()
				contents, next_page_exist, postfix = safe_queue.get(timeout=self._parse_contents_waiting_time)
				self.set_postfix(postfix)
				self.write_contents(hfile, contents)
				if (not next_page_exist) or (self._end_page and self._url == self._end_page):
					break
				self._reconnection_counter = 0
				self._random_wait(True)
				if self._verbose:
					print('----------------------------------over----------------------------------')
			except Exception as e:
				print('Exception occurred!!!')
				if isinstance(e, queue.Empty):
					proc.terminate()
					print('Method parse_and_write executed too much time, may be blocked by some reason, rerun.')
				else:
					print(e)
				self._random_wait(False)
				self._reconnection_counter += 1
				print(f'Reconnection counter {self._reconnection_counter}')
				if self._reconnection_counter >= self._reconnections_limit:
					print('Max reconnections exceed, exit!!!')
					print(f'Error url {self._url}')
					exit(1)
				continue

		print('finished!')
		hfile.close()

	# two methods must be overridden
	@staticmethod
	def parse(bsobj):
		"""
		Parse beautifulsoup object to get text and title
		:param bsobj: BS4 object
		:return: Contents(text, title, title_write_flag)
		"""
		return Contents('', '', False)

	@staticmethod
	def next_page(bsobj):
		"""
		Turn to next page with set_postfix() and set_full_url() methods
		:param bsobj: BS4 object
		:return: (bool, postfix), True means next page set okay, False means this whole activity is done (if end_page is set, this method can leave it behind)
		"""
		return False, None