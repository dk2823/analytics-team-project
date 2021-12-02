#!/usr/bin/python

from bs4 import BeautifulSoup
import requests, urllib.parse
import time
from dateutil import rrule
from datetime import datetime


# Note - Have to get your "User-Agent" if you didn't set it up
#      - It looks like Google News web changes the class name often. Need to double check the class for div tag you want to grab before running this script
#      - 36 page is the last page.
#      - News feeds from https://www.google.com/search

def paginate(url, keyword, dateToSearch, previous_url=None):
    # Break from infinite recursion
    if url == previous_url: return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    params = {
        "q": f"{keyword}",
        "hl": "en",
        "tbas": "0",
        "tbs": f"cdr:1,cd_min:{dateToSearch},cd_max:{dateToSearch},sbd:1",
        # "tbs": "sbd:1",
        "tbm": "nws",
        "source": "lnt"
    }

    response = requests.get(url, headers=headers, params=params).text
    soup = BeautifulSoup(response, 'lxml')

    # First page
    yield soup

    next_page_node = soup.select_one('a#pnnext')

    # Stop when there is no next page
    if next_page_node is None: return

    next_page_url = urllib.parse.urljoin('https://www.google.com/',
                                         next_page_node['href'])

    # Pages after the first one
    yield from paginate(next_page_url, keyword, dateToSearch, url)


def scrape():

    start = '20211009'
    end = '20211009'
    listOfDates = getDates(start, end)
    file = open("MyFile.txt", "a")
    keyword = "Apple"
    ticker = "APPL"

    for index, d in enumerate(listOfDates):
        print(index, d)
        pages = paginate("https://www.google.com/search?", keyword, d)

        for soup in pages:
            print(f'Current page: {soup.select_one(".YyVfkd").text}')
            # print()

            for data in soup.findAll('a', class_='WlydOe'): # <a> tag

                title = data.find('div', class_='mCBkyc JQe2Ld nDgy9d').text # div tag that has title
                link = data['href'] # a tag
                snippet = data.find('div', class_='GI74Re nDgy9d').text # div tag that has snippet
                published = data.find('p').find('span').text

                # file.write(f'{d}|{ticker}|{title}|{snippet}|{link}')
                # file.write('\n')
                print(f'Title: {title}')
                print(f'Link: {link}')
                print(f'snippet: {snippet}')
                print(f'published: {published}')
                print()
                # time.sleep(1)

        time.sleep(5)
        print("scripting news on " + d + " is done")

    print("it's done")
# date, ticker, title, snippet, link , ticker

def getDates(start, end):
    dates = []
    for dt in rrule.rrule(rrule.DAILY,
                          dtstart=datetime.strptime(start, '%Y%m%d'),
                          until=datetime.strptime(end, '%Y%m%d')):
        dates.append(dt.strftime('%m/%d/%Y'))

    return dates

scrape()
