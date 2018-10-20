#! python3

import sys
from time import time, strftime
from datetime import datetime
import networkx as nx
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import matplotlib.pyplot as plt
from random import shuffle



def main():
    crawl(False)


def getTitle(url):
    '''Gets the title of wikipedia article from url
    '''

    for i, char in enumerate(reversed(url)):

        if char == '/':
            start = i
            return url[(len(url)-start):]

    raise Exception('No valid title') 
    
def getLinks(browser, noLinks=False, xPath='//*[@id="mw-content-text"]/div/p[1]/a'):

    # for whole page use:      '//*[@id="mw-content-text"]/div'
    # for first paragraph use: 

    elems = browser.find_elements_by_xpath(xPath)
    
    for i, elem in enumerate(elems):  # get link text from element
        elems[i] = elem.get_attribute("href")

    if noLinks:  # if noLinks is None get all links
        try:
            elems = elems[0:noLinks]
        except:
            pass

    return elems

def saveNetwork(network, unvisitedWrite, networkWrite, unvisited, output=True):

    fp = open(unvisitedWrite, 'w+')

    for url in unvisited:
        fp.write('{}\n'.format(url))

    nx.write_gml(network, networkWrite)

    if output:
        print("Unvisited data saved to {}.".format(unvisitedWrite))
        print("Network saved to {}.".format(networkWrite))

def showNetwork(network):

    print('Close network display to output network variable')
    #pos = nx.spring_layout(network,k=0.15,iterations=20)
    nx.draw(network, with_labels=True)
    plt.show()

def setupDriver(headless=True):
    # setup driver
    options = webdriver.ChromeOptions()
    options.add_argument('log-level=3')  # remove output to console
    if headless: 
        options.add_argument('headless')
    return webdriver.Chrome(executable_path=r"C:/Users/Ben/OneDrive/Documents/Python/chromedriver.exe", chrome_options=options)

def crawl(seed=["https://en.wikipedia.org/wiki/Transistor"], depth=False, headless=True, load=False, \
    save=False, unvisitedWrite='unvisited.txt', networkWrite='network.gml', show=True, stopConnected=False):
    
    ''' starts at wikipedia page url specified by SEED and gets DEPTH links form 1st paragraph. CRAWL will then
        access wikipedia pages linked by previously visited pages.
        Also takes arguments:
            headless:       Default=True            -- Set to false for crawling to take place in physical browser window
            load:           Default=False           -- Set to true to load previous gml file
            save:           Default=False           -- set to true to save variables in format that allows crawling to continue
            unvisitedWrite: Default='unvisited.txt' -- file name to write list of univisited urls to if save=True
            network.Write:  Default='netowrk.gml'   -- file name of network if save=True
    '''

    browser = setupDriver(headless=headless)

    if(stopConnected):
        try:
            source = getTitle(seed[0])
            target = getTitle(seed[1])
        except:
            sys.exit('stopConnected argument requires SEED to be a list containing 2 wikipedia urls')

    ''' load file
    '''
    if load:
        unvisited = []
        try:  # try loading file
            fp = open(unvisitedWrite, 'r')
            ln = fp.readline().strip()
            while ln is not '':             # read urls from unvisiedWrite into unvisited
                ln = fp.readline().strip()
                unvisited.append(ln)
            fp.close()
        except IOError:
            sys.exit('''No file called '{}' . Re-run with load = False'''.format(unvisitedWrite))

        try:  # check if file specified exists
            network = nx.read_gml(networkWrite)
        except IOError: # if not raise error
            sys.exit('''No file called '{}'. re-run with load = False'''.format(networkWrite))
    else:        
        network = nx.DiGraph()  # create network        
        unvisited = seed  # seed unvisited list

    ''' Main try block. Break on KeyboardInterrupt
    '''
    try:
        startTime = time()
        minutes = 3
        if save:
            print('Saving progress every {} minutes'.format(minutes))
        print('crawling...\n\n')

        ''' Main crawl loop
        '''
        while True:
            currentUrl = unvisited[0]  # get next url

            ''' Check valid title
            '''
            try:  # try getting title
                fromTitle = getTitle(currentUrl) 
            except Exception:  # if not valid title get the next one
                unvisited.pop(0)
                currentUrl = unvisited[0]
                fromTitle = getTitle(currentUrl)

            browser.get(currentUrl)  # pull url

            ''' Check save condition
            '''
            if (time()-startTime >= 60*minutes) and save:
                startTime = time()
                saveNetwork(network, unvisitedWrite, networkWrite, unvisited, output=False)
                print('Saved at {}'.format(datetime.now().strftime('%I:%M%p')))
                print('Unvisited is currently {} items long'.format(len(unvisited)))
                print('Currently visiting {}'.format(fromTitle))
                print('crawling...\n\n')

            ''' Get next links from page
            '''
            links = getLinks(browser, noLinks=depth)  # get links from page
            unvisited = unvisited + links  # add links to unvisited

            ''' Create arc between articles and add to network
            '''
            for link in links:

                toTitle = getTitle(link)

                if toTitle not in network.nodes(): # check if toTitle is already in network
                    network.add_node(toTitle)      # if not then add it

                network.add_edge(fromTitle, toTitle) # create arc: fromTitle --> toTitle 
            
            unvisited.pop(0)  # remove source node from list

            # Stop when graph is connected condition
            
            if stopConnected:
                try:
                    nx.shortest_path(network, source, target)
                    print('Nodes connected')
                    return network
                except:
                    pass

    except KeyboardInterrupt:
        print('\n\nExecution Stopped')
        browser.quit()

    if save:
        saveNetwork(network, unvisitedWrite, networkWrite, unvisited)
    if show:
        showNetwork(network)

    return network

def shortestPath(source, target, network=True, fileName='network.gml'):
    ''' Computes shortest path from SOURCE to TARGET from file
        source: -- Source node. Must be valid wikipedia url
        target
    '''

    if type(network) == bool:
        try:
            network = nx.read_gml(fileName)
        except:
            sys.exit("file '{}' does not exist. Use network= to load network as variable".format(fileName))
    colourList = []
    
    # compute shortest path
    try:
        shortestNodes = nx.shortest_path(network, source, target)
    except:
        print('No valid path exists from {} to {}'.format(source, target))
        return None        

    # check node is in shortest path
    for node in network.nodes():
        if node in shortestNodes:
            colourList.append('green')
        else:
            colourList.append('red')

    edgeColours = []
    widths = []

    for edge in network.edges():
        if (edge[0] in shortestNodes) and (edge[1] in shortestNodes):
            edgeColours.append('green')
            widths.append(4)
        else:
            edgeColours.append('black')
            widths.append(0.5)

    returnString = '{}'.format(shortestNodes[0])
    shortestNodes.pop(0)

    for node in shortestNodes:
        returnString += ' --> {}'.format(node)


    pos = nx.spring_layout(network,k=0.15,iterations=20)
    nx.draw(network, pos=pos, with_labels=True, node_color=colourList, edge_color=edgeColours, width=widths)
    plt.show()

    return returnString

def readNetwork(filename='network.gml'):
    return nx.read_gml(filename)


if __name__ == "__main__":
    main()