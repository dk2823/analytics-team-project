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

def paginate(url, keyword, dateToSearch, numPages, count, previous_url=None):
    # Check if the page count reaches to the number of pages we limit
    if count >= numPages: return

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
    count += 1
    soup = BeautifulSoup(response, 'lxml')

    # First page
    yield soup

    next_page_node = soup.select_one('a#pnnext')

    # Stop when there is no next page
    if next_page_node is None: return

    next_page_url = urllib.parse.urljoin('https://www.google.com/',
                                         next_page_node['href'])

    # Pages after the first one
    yield from paginate(next_page_url, keyword, dateToSearch, numPages, count, url)


def scrape():

    start = '20161027'
    end = '20211027'
    # today = '20211103'
    listOfDates = getDates(start, end)
    file = open("testOnlyFirstPagesADI.csv", "a")
    errorLog = open("error_log.txt", "a")

    keyword = "analog devices"
    ticker = "ADI"
    numPages = 1

    for index, d in enumerate(listOfDates):
        count = 0
        print(index, d, ticker)
        pages = paginate("https://www.google.com/search?", keyword, d, numPages, count)

        for soup in pages:
            try:
                for data in soup.findAll('a', class_='WlydOe'): # <a> tag

                    title = data.find('div', class_='mCBkyc JQe2Ld nDgy9d').text # div tag that has title
                    link = data['href'] # a tag
                    snippet = data.find('div', class_='GI74Re nDgy9d').text # div tag that has snippet
                    snippet = snippet.replace("\n", " ")
                    published = data.find('p').find('span').text

                    file.write(f'{d}|{ticker}|{title}|{snippet}|{link}')
                    file.write('\n')
                    # print(f'Title: {title}')
                    # print(f'Link: {link}')
                    # print(f'snippet: {snippet}')
                    # print(f'published: {published}')
                    # print()
            except Exception:
                errorLog.write("Cannot get data from google. it's blocked at " + str(datetime.now()))
                print("Cannot get data from google. it's blocked at " + str(datetime.now()))


        time.sleep(5)

    print("it's done")

def getDates(start, end):
    dates = []
    for dt in rrule.rrule(rrule.DAILY,
                          dtstart=datetime.strptime(start, '%Y%m%d'),
                          until=datetime.strptime(end, '%Y%m%d')):
        dates.append(dt.strftime('%m/%d/%Y'))

    return dates

scrape()
