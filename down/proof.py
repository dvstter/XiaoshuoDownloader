# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

"""
	Use this class to get beautifulsoup object, then develop the extraction and next_page method!
"""
class Dev:
  def __init__(self, url):
    self.url = url
    self.Headers = {
      "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
      "cache-control": "no-cache",
      "accept-encoding": "gzip, deflate"}
    self.Proxies = {"http":"http://127.0.0.1:1087", "https":"https://127.0.0.1:1087"}
    
  def getbs(self, gbk=True):
    print(f"Fetching {self.url}")
    resp = requests.get(self.url, headers=self.Headers, proxies=self.Proxies)
    if gbk:
      return BeautifulSoup(resp.text.encode("iso-8859-1").decode('gbk', "ignore"), "lxml")
    else:
      return BeautifulSoup(resp.text, "lxml")
