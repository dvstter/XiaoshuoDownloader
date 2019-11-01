# -*- coding:utf-8 -*-
import requests
import time
import re
import random
from bs4 import BeautifulSoup

Base = "http://m.12bz.org"
Postfix = "/7_7933/109289.html"
Endpage = "/7_7933/"
Headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36", 
        "cache-control":"no-cache", 
        "accept-encoding":"gzip, deflate"}
Proxies = {"http":"http://127.0.0.1:1087", "https":"https://127.0.0.1:1087"}

def get_data(hfile):
    next_postfix = Postfix
    while True:
        next_postfix = request_data(next_postfix, hfile)
        if not next_postfix:
            break
        w_tm = random.randint(0, 5)
        print(f"Waiting for {w_tm} secs")
        time.sleep(w_tm)

def request_data(url_postfix, hfile):
    url = Base + url_postfix
    print("--------------------------------------------------------")
    print(f"Fetching {url}")
    resp = requests.get(url, headers=Headers, proxies=Proxies)
    bs = BeautifulSoup(resp.text, "lxml")
    try:
        text = bs.find_all("div", id="nr1").text
        text = re.sub(r"&[a-z;]+", "", text)
        text = re.sub(r"<[a-z]+?>", "", text)
        hfile.write(text)
        hfile.write("\n\n")
        hfile.flush()
        print(f"Finish current page")

        next_postfix = None
        for each in bs.find("a", id="pb_next"):
            if each["href"] != Endpage:
                next_postfix = each["href"]
        return next_postfix
    except IndexError as _:
        f = open("error_page_source.txt", "w", encoding="utf-8")
        f.write(resp.text)
        f.close()
        print("IndexError occured!")
        return True

if __name__ == "__main__":
    f = open("xiaoshuo.txt", "a", encoding="utf-8")
    get_data(f)
    
