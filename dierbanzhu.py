# -*- coding:utf-8 -*-
from down.generic import GenericDownloader

class Downloader(GenericDownloader):
	def __init__(self, output_file):
		super().__init__("http://www.diershubao.org", "/0_10/4783.html", gbk=True, output=output_file)
	
	def extraction(self, bsobj):
		content = bsobj.find("div", id="content")
		result = ""
		for each in content.children:
			if not each.name:
				result += each
				
		return result
	
	def next_page(self, bsobj):
		for each in bsobj.find_all("a"):
			if each.text == "下一章":
				self.setpostfix(each["href"])
				
		return True

if __name__ == "__main__":
	dn = Downloader("xiaoshuo.txt")
	dn.run()

