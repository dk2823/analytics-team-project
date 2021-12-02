#!/usr/bin/python

import sys
from requests_html import HTMLSession
import bs4
from bs4 import BeautifulSoup
import time
from datetime import datetime


# news feeds from https://finviz.com/quote.ashx?t=

def get_titles_links(tickers):
    url = "https://finviz.com/quote.ashx?t="
    s = HTMLSession()
    curr_date = str(datetime.now().strftime('%Y-%m-%d'))
    file = open("finviz-" + curr_date + ".csv", "a")
    d = str(datetime.now().strftime('%Y%m%d'))

    for each_ticker in tickers:
        print(each_ticker)
        r = s.get(url + each_ticker)
        soup = bs4.BeautifulSoup(r.html.html, 'html5lib')

        for each in soup.findAll('a', {'class': 'tab-link-news'}):
            title = each.getText().replace("\n", " ")
            link = each['href']
            file.write(f'{d}|{each_ticker}|{title}|{link}')
            file.write('\n')
            # print(f'Title: {title}')
            # print(f'Link: {link}')
            # print()

def getCurrData(lst):
    get_titles_links(lst)

def getList(filename):
    lst = []
    first_line = True
    with open(filename) as f:
        for line in f:
            if first_line:
                first_line = False
            else:
                val = line.split(',')
                lst.append(val[0])

    return lst

def main(argv):
    lst = []

    if len(sys.argv) < 2:
        filename = "nasdaq_tickers.csv"
        lst = getList(filename)
    else:
        lst = getList(argv[1])

    getCurrData(lst)
    print("It's done")

if __name__ == "__main__":
    main(sys.argv)