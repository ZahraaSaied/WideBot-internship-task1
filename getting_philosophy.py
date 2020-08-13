# -*- coding: utf-8 -*-

import requests, re
from bs4 import BeautifulSoup
import time

def getting_philosophy(url):
    LIMIT = 50
    n = 0
    visited_urls = []

    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    # Print current url
    print(r.url)

    while soup.findAll('h1', {'class':'firstHeading'})[0].contents[0] != 'Philosophy':
        if n == LIMIT:
            print("Limit of 50 redirectionss is reached!")
            return None

        content = soup.find(id='mw-content-text')
        for t in content.find_all(class_=['navbox', 'vertical-navbox', 'toc']):
            t.replace_with("")

        paragraph = soup.select('div.mw-parser-output > p')[0]
        for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']):
            s.replace_with("")
        paragraphText = str(paragraph)
        paragraphText = re.sub(r' \(.*?\)', '', paragraphText)

        # print(paragraphText)

        reParagraph = BeautifulSoup(paragraphText)
        firstLink = reParagraph.find(href=re.compile('^/wiki/'))

        while firstLink == None:
            # case of disambiguation: use first wiki link in list
            if '(disambiguation)' in url or '(surname)' in url:
                firstLink = content.ul.find(href=re.compile('^/wiki/'))

            else:
                paragraph = paragraph.find_next_sibling("p")

                if (paragraph is None):
                    if (content.ul is not None):
                        firstLink = content.ul.find(href=re.compile('^/wiki/'))  
                    
                    # No links available  
                    if (firstLink is None):  
                        print("Wikipedia link not reachable!")
                        return None
                    continue

                for s in paragraph.find_all(['span', 'small', 'sup,', 'i', 'table']):
                    s.replace_with("")
                paragraphText = str(paragraph)
                paragraphText = re.sub(r' \(.*?\)', '', paragraphText)
                reParagraph = BeautifulSoup(paragraphText)
                firstLink = reParagraph.find(href=re.compile('^/wiki/'))

        url = 'http://en.wikipedia.org' + firstLink.get('href')
        print(url)
        
        # break befor stucking in a loop
        if url in visited_urls:
            print("Break - Stuck in a loop!")
            return None
        
        visited_urls.append(url)
        # Make new request
        r = requests.get(url)  
        soup = BeautifulSoup(r.text)

        n = n + 1
        time.sleep(0.5)

    print(str(n) + " redirections to reach Philosophy!")
    return None

# Testing func
getting_philosophy('http://en.wikipedia.org/wiki/Special:Random')

