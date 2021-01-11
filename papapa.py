# -*- coding:utf-8 -*-
from down.generic import GenericDownloader

class Downloader(GenericDownloader):
	def __init__(self, output_file):
		super().__init__("http://www.papapa.biz", "/chenpipi/000001.html", gbk=True, output=output_file)
	
	def extraction(self, bsobj):
		result = bsobj.find('h1').text
		content = bsobj.find("div", id="content").text
		result += content

		return result
	
	def next_page(self, bsobj):
		for each in bsobj.find_all("a"):
			if each.text == "下一章":
				self.setpostfix(each["href"])
				
		return True

if __name__ == "__main__":
	dn = Downloader("xiaoshuo.txt")
	dn.run()

