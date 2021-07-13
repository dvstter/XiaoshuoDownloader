# _*_ coding: utf-8 _*_
import requests
import time
import random
from bs4 import BeautifulSoup as BS
from requests.exceptions import RequestException


class DownloaderSignal(Exception):
    TYPE_RECONNECT = 0
    def __init__(self, type=TYPE_RECONNECT):
        super(DownloaderSignal, self).__init__()
