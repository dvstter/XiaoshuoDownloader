# -*- coding:utf-8 -*-
from down.generic_legacy import *
import re
from copy import deepcopy

class Downloader(GenericDownloader):
  def __init__(self, output_file):
    super().__init__('https://m.xinyushuwu.org', '/17/17997/848674.html', output=output_file)

  def extraction(self, bsobj):
    content = bsobj.find('div', id='novelcontent')
    content = deepcopy(content)
    content.find('ul', class_='novelbutton').decompose()
    if not content:
      return DownloaderSignal.REPEAT, None
    text = content.text.strip()
    text = re.sub(r'\s+', '\n\n', text)

    title = bsobj.find('h1', id='chaptertitle').text.strip()
    write_title_flag = re.findall(r'([0-9]+)/[0-9]+', title)
    if len(write_title_flag):
      write_title_flag = int(write_title_flag[0]) == 1

    result = ExtractionContent(text, title, write_title_flag)
    return DownloaderSignal.OK, result

  def grep(self, text):
    text = re.sub(r'&nbsp;', '', text)
    text = re.sub(r'<br>', '\n', text)
    return text

  def next_page(self, bsobj):
    next_item = bsobj.find('ul', class_='novelbutton')
    postfix = next_item.find('p', 'p1 p3').a['href']
    if postfix == '/17/17997/':
      return False
    else:
      self.set_postfix(postfix)
      return True

if __name__ == '__main__':
  dn = Downloader('xiaoshuo.txt')
  dn.run()

