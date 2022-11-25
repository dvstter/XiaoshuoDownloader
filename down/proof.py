# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

Headers = {
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
  'cache-control': 'no-cache',
  'accept-encoding': 'gzip, deflate'}
Proxies = {'http': 'http://127.0.0.1:7890'}

def get_bs(url, proxy=True, gbk=False):
  print(f'Fetching {url}')
  resp = requests.get(url, headers=Headers, proxies=Proxies) if proxy else requests.get(url, headers=Headers)
  return BeautifulSoup(resp.text.encode('iso-8859-1').decode('gbk', 'ignore'), 'lxml') if gbk else BeautifulSoup(resp.text, 'lxml')
