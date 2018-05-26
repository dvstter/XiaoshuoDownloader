# -*- coding:utf-8 -*-
import requests
import time
import re
import random
from bs4 import BeautifulSoup

Base = "http://www.sanhaoxs.org/0_234/{}.html"
#Counter = 17281
Counter = 158438
Headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36", 
        "cache-control":"no-cache", 
        "accept-encoding":"gzip, deflate"}
Proxies = {"http":"http://127.0.0.1:1087", "https":"https://127.0.0.1:1087"}

def get_data(hfile):
    cnt = 1
    while True:
        if not request_data(cnt, hfile):
            break
        w_tm = random.randint(0, 5)
        print(f"Waiting for {w_tm} secs")
        time.sleep(w_tm)
        cnt += 1

def request_data(page_cnt, hfile):
    url = Base.format(Counter + page_cnt - 1)
    print(f"Fetching url {url}")
    resp = requests.get(url, headers=Headers, proxies=Proxies)
    bs = BeautifulSoup(resp.text.encode("iso-8859-1").decode('gbk', "ignore"), "lxml")
    try:
        text = bs.find_all("div", id="content")[0].text
        text = re.sub(r"&[a-z;]+", "", text)
        text = re.sub(r"<[a-z]+?>", "", text)
        hfile.write(text)
        hfile.write("\n\n")
        hfile.flush()
        print(f"Finish page {page_cnt}")

        for each in bs.find_all("a"):
            if each.text == "下一章":
                if each["href"] == "/0_234/":
                    return False
        return True
    except IndexError as _:
        f = open("error_page_source.txt", "w", encoding="utf-8")
        f.write(resp.text.encode("iso-8859-1").decode("gbk"))
        f.close()
        print("IndexError occured!")
        return True

if __name__ == "__main__":
    f = open("xiaoshuo.txt", "a", encoding="utf-8")
    get_data(f)
    
