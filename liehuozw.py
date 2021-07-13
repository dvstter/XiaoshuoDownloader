# -*- coding:utf-8 -*-
from down.generic import *


class Downloader(GenericDownloader):
    def __init__(self, output_file):
        super().__init__('http://m.bz001.cc', '/2_2123/125235_2.html', 'http://m.bz001.cc/2_2123/', gbk=True, output=output_file)

    def extraction(self, bsobj):
        content = bsobj.find('div', id='novelcontent')
        # need to complish later
        title = bsobj.find
        C = ExtractionContent(content, title, flag)
        if content:
            return DownloaderSignal.OK, C
        else:
            return DownloaderSignal.REPEAT, None

    def next_page(self, bsobj):
        for each in bsobj.find_all('a'):
            if each.text == '下一章' or each.text == '下一页':
                self.setpostfix(each['href'])

        return True


if __name__ == '__main__':
    dn = Downloader('xiaoshuo.txt')
    dn.run()

