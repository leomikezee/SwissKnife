#!/usr/bin/python
"""Simple Currency Comverter"""

from __future__ import print_function

from urllib.request import urlopen
from urllib.error import URLError
from html.parser import HTMLParser
from sys import argv

FROM = "https://www.google.com/finance/converter?a=1&from="
TO = "&to="
CONNECTION_MSG = "Cannot connect to Google Currency Converter!"
INPUT_MSG ="""Invalid arguments: {}\n---------
Examples:
		$ CurrencyConverter
		$ CurrencyConverter CAD CNY
		$ CurrencyConverter 10 USD CNY
"""

class CurrencyParser(HTMLParser):
	# Extract data (including nested data) from tag with id = currency_converter_result
	def __init__(self):
		HTMLParser.__init__(self)
		self.recording = 0
		self.data = []

	def handle_starttag(self, tag, attributes):
		if tag != 'div':
			return
		if self.recording:
			self.recording += 1
			return
		for name, value in attributes:
			if name == 'id' and value == 'currency_converter_result':
				break
		# Loop statements may have an else clause;
		# it is executed when the loop terminates through
		# exhaustion of the list (with for) or 
		# when the condition becomes false (with while)
		# So 'break' will ignore the else clause
		else:
			return
		self.recording = 1

	def handle_endtag(self, tag):
		if tag == 'div' and self.recording:
			self.recording -= 1

	def handle_data(self, data):
		if self.recording:
			self.data.append(data)

# Get HTML from Google Currency Converter
def getResult(url):
	try:
		response = urlopen(url)
	except (URLError, IOError) as e:
		print(CONNECTION_MSG)
		return
	result = response.read()
	response.close()
	return result

def printResult(url):
	result = getResult(url)
	p = CurrencyParser()
	print(result)
	p.feed(result)
	for i in p.data:
		print(i, end="")

def main(args = argv[1:]):
	# 0 argument
	if len(args) == 0:
		url = FROM + "CAD" + TO + "CNY"
		printResult(url)
		url = FROM + "USD" + TO + "CNY"
		printResult(url)
	# 2 arguments
	elif len(args) == 2:
		url = FROM + args[0] + TO + args[1]
		printResult(url)
	# 3 arguments
	elif len(args) == 3 and args[0].isdigit():
		url = FROM.replace("1", args[0]) + args[1] + TO + args[2]
		printResult(url)
	# invalid arguments
	else:
		print(INPUT_MSG)

if __name__ == '__main__':
	main()
