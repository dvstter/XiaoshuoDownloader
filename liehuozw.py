# -*- coding:utf-8 -*-
from down.generic import GenericDownloader


class Downloader(GenericDownloader):
    def __init__(self, output_file):
        super().__init__("https://m.liehuozw.com", "/0/142/197086.html", 'https://m.liehuozw.com/0/142/', gbk=False, output=output_file)

    def extraction(self, bsobj):
        content = bsobj.find("div", id="novelcontent")
        return content.text

    def next_page(self, bsobj):
        for each in bsobj.find_all("a"):
            if each.text == "下一章" or each.text == '下一页':
                self.setpostfix(each["href"])

        return True


if __name__ == "__main__":
    dn = Downloader("xiaoshuo.txt")
    dn.run()

