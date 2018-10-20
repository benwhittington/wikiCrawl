#! python2

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from random import shuffle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.options import Options

def getTitle(url):
	start = []
	for i, char in enumerate(reversed(url)):

		if char == '/':
			start = i
			break
	title = url[len(url)-start:len(url)]
		
	return title

def getLinks(browser, noLinks):	
	pageLinks = browser.find_elements_by_xpath('//*[@id="mw-content-text"]/div/p[1]/a')
	shuffle(pageLinks)
	nextLinks = pageLinks[0:noLinks]
	return nextLinks

def showConnection(adjMat, currentPageUrl, url, titles):
	# add column to adjMat
	adjMat = np.concatenate((adjMat, np.transpose([np.zeros(adjMat.shape[0])])), 1)
	urlTitle = getTitle(url)
	currentTitle = getTitle(currentPageUrl)

	# if url title is in titles add 1 to existing row
	if urlTitle in titles:
		row = adjMat.shape[0]-1
		col = titles.index(urlTitle) - 1
		adjMat[row, col] = 1
	else:
		# add row to adjMat
		adjMat = np.concatenate((adjMat, ([np.zeros(adjMat.shape[1])])), 0)
		row = adjMat.shape[0]-1
		col = adjMat.shape[1]-1
		adjMat[row, col] = 1

	return adjMat	
		


browser = webdriver.Chrome()


#chrome_options = Options()  
#chrome_options.add_argument("--headless")  
#chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'   
#browser = webdriver.Chrome(executable_path='C:\Users\\benji\AppData\Local\Google\Chrome SxS\Application',   chrome_options=chrome_options)


#setupHeadless

print("done")
startUrl = "https://en.wikipedia.org/wiki/Transistor"
titles = [getTitle(startUrl)]

visitedUrls = []
unvisited = []

unvisited.append(startUrl)
adjMat = np.matrix([[0]])
count = 0
depth = 5

# begin function
# visit top url
while count < 100:

	# url at top of list
	currentPageUrl = unvisited[0]
	# go to page
	browser.get(currentPageUrl)

	# get links from first paragraph
	pageUrls = getLinks(browser, depth)

	# loop through each url from browser
	for url in pageUrls:
		# get actual url text
		url = url.get_attribute("href")

		# check if url is already visited or we are already about to visit it
		if ~(url in unvisited) and ~(url in visitedUrls):
			# add to list of unvisited urls
			unvisited.append(url)
			# append current page url to visited urls
			visitedUrls.append(currentPageUrl)
			# add connection to adjMat
			adjMat = showConnection(adjMat, currentPageUrl, url, titles)	
			# add title if not already in titles
			if ~(getTitle(url) in titles):
				titles.append(getTitle(url))

	# pop current url from list	
	unvisited = unvisited[1:len(unvisited)]


	count += 1


browser.close()


# make adjmat square
while adjMat.shape[0] != adjMat.shape[1]:
	adjMat = np.concatenate((adjMat, ([np.zeros(adjMat.shape[1])])), 0)

pos = {}

for i, title in enumerate(titles):
	pos[i] = str(title)	

g = nx.from_numpy_matrix(adjMat)
#pos = nx.spring_layout(g)

#nx.draw_networkx_labels(G, pos)
#nx.set_node_attributes(g, pos)

nx.draw(g)
plt.show()
