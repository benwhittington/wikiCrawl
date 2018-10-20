from functions import *


url1 = 'https://en.wikipedia.org/wiki/Resource_(biology)'
url2 = 'https://en.wikipedia.org/wiki/Chemistry'
title1 = getTitle(url1)
title2 = getTitle(url2)

seed = [url1, url2]

# network = crawl(seed=seed, save=True, show=False, stopConnected=True)
network = readNetwork()

print(shortestPath(title1, title2, network=network))
#print(shortestPath(title2, title1, network=network))
