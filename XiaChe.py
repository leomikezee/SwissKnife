#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Simple Zhihu XiaChe Reader"""

from urllib.request import urlopen
from urllib.error import URLError
from html.parser import HTMLParser
from json import loads

CONNECTION_MSG = "Cannot connect to Zhihu!"
LIST_URL = "http://news-at.zhihu.com/api/3/news/latest"
CONTENT_URL = "http://news-at.zhihu.com/api/4/news/"

class XiaCheParser(HTMLParser):
	# Extract data from tag <h2> and <p>
	# Insert a newline before <h2> for easy reading
	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0
		self.data = []

	def handle_starttag(self, tag, attributes):
		if tag == u'h2':
			self.recording = 1
		elif tag == u'p':
			self.recording = 2

	def handle_endtag(self, tag):
		self.recording = 0

	def handle_data(self, data):
		if self.recording == 1:
			self.data.append('\n')
			self.data.append(data)
		elif self.recording == 2:
			self.data.append(data)

# Get JSON from ZhiHu API
def getResult(url):
	try:
		response = urlopen(url)
	except (URLError, IOError) as e:
		print(CONNECTION_MSG)
		return
	result = response.read()
	response.close()
	return result

# Parse JSON to get proper ID for XiaChe
def getID(url):
	parsedJSOM = loads(getResult(url))
	for i in parsedJSOM["stories"]:
		# \u778e\u626f is unicode of XiaChe
		if u'\u778e\u626f' in i["title"]:
			return str(i["id"])

def printResult(url):
	parsedJSOM = loads(getResult(url))
	html = parsedJSOM["body"]
	p = XiaCheParser()
	p.feed(html)
	p.data.append('\n')
	for i in p.data:
		print(i)
		# print(unicode(i).encode('utf8'))

def main():
	printResult(CONTENT_URL + getID(LIST_URL))

if __name__ == '__main__':
	main()
