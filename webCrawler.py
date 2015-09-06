import requests
import re

disallowList = []

def addToCSV(url, title, children):
	print("RAJ_DEBUG:", url,' - ', title, ' - ', children)

def appendDisallowList(url):
	user_agent = {'User-agent': 'Testbot'}
	rgets = requests.get(url+'/robot.txt')
	collect = 0
	for i in str(rgets.content).split('\\n'):
		if re.search('User-agent: \*', i) != None or \
			re.search('User-agent: Testbot', i) != None:
			collect = 1
		elif re.search('User-agent:', i) != None:
			collect = 0
		if collect == 1 and re.search('Disallow:', i) != None:
			disallowList.append(i.split(' ')[1])

def crawl_web(initial_url):
	crawled, to_crawl = [], []
	to_crawl.append(initial_url)
	while to_crawl:
		title = []
		current_url = to_crawl.pop(0)
		children = 0
		r = requests.get(current_url)
		title = re.findall('<title>(.*?)</title>', str(r.content))
		crawled.append(current_url)
		for url in re.findall('href="([^"]+)">', str(r.content)):
			if url[0] == '/':
				url = current_url + url[1:]
			pattern = re.compile('https?')
			if pattern.match(url) and url not in disallowList:
				to_crawl.append(url)
			children = children + 1
		yield current_url
		if len(title) > 0 : 
			addToCSV(current_url, title[0], children)
		else:
			addToCSV(current_url, '', children)

appendDisallowList('http://ctogden.com')
crawl_web_generator = crawl_web('http://ctogden.com')
for result in crawl_web_generator:
	print(result)
	print
