# -*- coding:utf-8 -*-
from down.generic import *
import re
import pickle
from multiprocessing import Queue
from copy import deepcopy

class Downloader(GenericDownloader):
  """
  This is a demonstration for that which firstly scrawl the directory list and then scrawl the content
  """
  def __init__(self, output_file):
    super().__init__('xxxxx', '/xxx.html', output=output_file, verbose=False) # directory list url
    # these two attributes must be public
    self.directory_list = []
    self.directory_list_done = False
    self.idx = 0

  @staticmethod
  def parse(bsobj, dlobj):
    if dlobj.directory_list_done:
      # parse the page content, like this
      #return Contents(text, title, write_title_flag)
      pass
    else:
      # parse the directory list
      return Contents('', '', False)

  @staticmethod
  def next_page(bsobj, dlobj):
    if dlobj.directory_list_done:
      postfix = dlobj.split_url(dlobj.directory_list[dlobj.idx])
      return True, postfix
    else:
      # find next page for directory list page
      return True, postfix