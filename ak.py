# -*- coding:utf-8 -*-
from down.generic_backup import *


class Downloader(GenericDownloader):
  def __init__(self, output_file):
    super().__init__('http://www.06ak.com', '/book/185580/42166745.html', output=output_file)

  def extraction(self, bsobj):
    content = bsobj.find('article', id='article')
    if content is None:
      return DownloaderSignal.REPEAT, None
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
    next_item = bsobj.find('a', id='next_url')
    if next_item.text.strip() == '没有了':
      return False
    else:
      self.setpostfix(next_item['href'])
      return True


if __name__ == '__main__':
  dn = Downloader('xiaoshuo.txt')
  dn.run()

