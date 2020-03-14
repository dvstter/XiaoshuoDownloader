# -*- coding:utf-8 -*-
import requests
import time
import random
from bs4 import BeautifulSoup

Baseurl = "http://www.diershubao.org/wanben/1_{}"
Headers = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
  "cache-control": "no-cache",
  "accept-encoding": "gzip, deflate"}
Proxies = {"http": "http://127.0.0.1:1087", "https": "https://127.0.0.1:1087"}

def get_novel_list(output):
	x = 1
	novelurls = {}
	while True: # need to modify to while, and change the x in the try-loop
		url = Baseurl.format(x)
		resp = requests.get(url, headers=Headers, proxies=Proxies)
		print("Fetching {}".format(url))
		try:
			bs = BeautifulSoup(resp.text.encode("iso-8859-1").decode('gbk', "ignore"), "lxml")
			for each in bs.find_all("span", class_="s2"):
				tag = each.find("a")
				novelurls[tag.text] = tag["href"]
			x += 1
			if x > 16:
				break
		except Exception as e:
			time.sleep(random.randint(6, 10))
			continue
	
	# write to file
	f = open(output, "wt")
	for each in novelurls.keys():
		f.write("{}|{}\n".format(each, novelurls[each]))
		
def filter_long_novel(input, output):
	f = open(input, "rt")
	f2 = open(output, "wt")
	for l in f.readlines():
		name, url = l.split("|")
		while True:
			try:
				print("Fetching {} -- {}".format(name, url))
				resp = requests.get(url, headers=Headers, proxies=Proxies)
				bs = BeautifulSoup(resp.text.encode("iso-8859-1").decode('gbk', "ignore"), "lxml")
				chs = len(bs.find_all("dd"))
				if chs == 0:
					continue
				f2.write("{}|{}\n".format(name, chs))
				f2.flush()
				break
			except Exception as e:
				print("--------------ERROR!!!")
				time.sleep(random.randint(6, 10))
				continue
		
		time.sleep(random.randint(5, 30)/10)

if __name__ == "__main__":
	#get_novel_list("list.txt")
	filter_long_novel("list.txt", "list_cha.txt")

