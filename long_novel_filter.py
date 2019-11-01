# -*- coding:utf-8 -*-
import requests
import time
from tqdm import tqdm
import random
from bs4 import BeautifulSoup

AuthorPage = "http://m.12bz.org/author/%E5%B0%8F%E5%BC%BA"
Headers = {
  "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
  "cache-control": "no-cache",
  "accept-encoding": "gzip, deflate"}
Proxies = {"http": "http://127.0.0.1:1087", "https": "https://127.0.0.1:1087"}

def get_novel_list(handler):
  resp = requests.get(AuthorPage, headers=Headers, proxies=Proxies)
  print("------------------------------------------------")
  print(f"Fetch all novels' list")
  bs = BeautifulSoup(resp.text, "lxml")
  for each in tqdm(bs.find_all("a", {"class": "blue"})):
  #for each in bs.find_all("a", {"class": "blue"}):
    link = "http://m.12bz.org"+each.get("href")
    title = each.text

    chap_num = get_chap_num(link)
    #print(f">>> Chapter nums -- {chap_num}")
    if chap_num >= 15:
      handler.write(f"{link} {title} {chap_num}\n")
    time.sleep(random.randint(0, 5) * 0.1)

  handler.close()
  print(f"Finished")
  print("------------------------------------------------")

def get_chap_num(link):

  resp = requests.get(link, headers=Headers, proxies=Proxies)
  #print(f">>> Testing {title}")
  bs = BeautifulSoup(resp.text, "lxml")
  try:
    return len(bs.find_all("ul", {"class": "chapter"})[1].find_all("li"))
  except Exception as _:
    return 0

if __name__ == "__main__":
  h = open("result.txt", "wt")
  get_novel_list(h)

