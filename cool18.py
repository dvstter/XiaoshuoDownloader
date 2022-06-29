# -*- coding:utf-8 -*-
from down.generic_backup import *


class Downloader(GenericDownloader):
  def __init__(self, output_file):
    super().__init__('https://www.cool18.com', '/bbs4/index.php?app=forum&act=threadview&tid=14049915', output=output_file)
    self._first_round = True
    self._all_pages = []

  def extraction(self, bsobj):
    content = bsobj.find('pre')
    for invalid in content.find_all('font'):
      invalid.decompose()

    if content is None:
      return DownloaderSignal.REPEAT, None

    if self._first_round:
      # extract all the pages
      urls = content.find('b').find_all('a')
      self._all_pages = reversed([u.href for u in urls])
      self._first_round = False
      content.find('b').decompose()
    texts = ''
    for each in content.children:
      txt = each.text.strip()
      if txt == '':
        texts += '\n\n'
      else:
        texts += txt

    texts = texts.strip() + '\n\n'

    title = bsobj.find('p', class_='style_h1').text.strip()

    result = ExtractionContent(texts, title, True)
    return DownloaderSignal.OK, result

  def next_page(self, bsobj):
    if len(self._all_pages) == 0:
      return False
    else:
      next_url = self._all_pages[0] # fetch next url
      self._all_pages = self._all_pages[1:] # remove this url
      self.set_whole_url(next_url)
      return True


if __name__ == '__main__':
  dn = Downloader('xiaoshuo.txt')
  dn.run()

