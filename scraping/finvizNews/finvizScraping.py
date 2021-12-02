#!/usr/bin/python

import sys
from requests_html import HTMLSession
import bs4
from bs4 import BeautifulSoup
import time

# news feeds from https://finviz.com/quote.ashx?t=

def get_titles_links(ticker):
    url = "https://finviz.com/quote.ashx?t=" + ticker

    s = HTMLSession()
    r = s.get(url)

    soup = bs4.BeautifulSoup(r.html.html, 'html5lib')

    stories = []
    for each in soup.findAll('a', {'class': 'tab-link-news'}):
        title = each.getText()
        link = each['href']
        story = {
            'title': title,
            'link': link
        }
        stories.append(story)
        print(f'Title: {title}')
        print(f'Link: {link}')
        print()
        time.sleep(1)

    return stories



def main(argv):
    if len(sys.argv) != 2:
        print("Please provide ticker.")
        sys.exit()
    else :
        get_titles_links(argv[1])


if __name__ == "__main__":
    main(sys.argv)