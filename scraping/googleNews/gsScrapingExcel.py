#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
import requests, urllib.parse
import time
from dateutil import rrule
from datetime import datetime
from datetime import timedelta

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


def scrape(lst, dates, old=None):

    errorLog = open("error_log.txt", "a")
    numPages = 1
    combined = True

    if old == None:
        old = ""

    for idx_cmp, t in enumerate(lst):
        if combined:
            file = open("newsData10days.csv", "a")
        else:
            file = open("newsData/newsData_" + t[0] + old + ".csv", "a")

        for index, d in enumerate(dates):
            count = 0
            print(index, d, t)
            pages = paginate("https://www.google.com/search?", t[1], d, numPages, count)

            for soup in pages:
                if len(soup(text=lambda t: "detected unusual traffic" in t)) > 0:
                    print(soup(text=lambda t: "detected unusual traffic" in t))
                    sys.exit()

                try:
                    for data in soup.findAll('a', class_='WlydOe'): # <a> tag

                        title = data.find('div', class_='mCBkyc').text # div tag that has title
                        title = title.replace("\n", " ")
                        link = data['href'] # a tag
                        snippet = data.find('div', class_='GI74Re nDgy9d').text # div tag that has snippet
                        snippet = snippet.replace("\n", " ")
                        published = data.find('p').find('span').text

                        file.write(f'{d}|{t[0]}|{title}|{snippet}|{link}')
                        file.write('\n')
                        # print(f'Title: {title}')
                        # print(f'Link: {link}')
                        # print(f'snippet: {snippet}')
                        # print(f'published: {published}')
                        # print()
                except Exception:
                    errorLog.write("Cannot get data from google. it's blocked at " + str(datetime.now()))
                    print("Cannot get data from google. it's blocked at " + str(datetime.now()))


            # time.sleep(5)

        file.close()
    print("it's done")

def getDates(start, end):
    dates = []
    for dt in rrule.rrule(rrule.DAILY,
                          dtstart=datetime.strptime(start, '%Y%m%d'),
                          until=datetime.strptime(end, '%Y%m%d')):
        dates.append(dt.strftime('%m/%d/%Y'))

    return dates

def getList(lst):
    keywordList = []
    for each in lst:
        splitStr = each.split(",")
        keywordList.append((splitStr[0], splitStr[1]))

    return keywordList

def get5yearsOfData(lst):
    dt = datetime.now()
    dt = dt.replace(year=dt.year-5)

    dates = getDates(str(dt.strftime('%Y%m%d')), str(datetime.now().strftime('%Y%m%d')))
    scrape(lst, dates, "5years")

def get10DaysOfData(lst):
    d = timedelta(days=10)
    dt = datetime.now() - d

    dates = getDates(str(dt.strftime('%Y%m%d')), str(datetime.now().strftime('%Y%m%d')))
    scrape(lst, dates)

def getCurrData(lst):
    scrape(lst, getDates(str(datetime.now().strftime('%Y%m%d')), str(datetime.now().strftime('%Y%m%d'))))

def getList(filename):
    lst = []
    first_line = True
    with open(filename) as f:
        for line in f:
            if first_line:
                first_line = False
            else:
                val = line.split(',')
                lst.append((val[0], val[1]))

    return lst


def main(argv):
    lst = []

    if len(sys.argv) < 2:
        filename = "nasdaq_tickers_s_13.csv"
        lst = getList(filename)
    else:
        lst = getList(argv[1])

    get10DaysOfData(lst)

if __name__ == "__main__":
    main(sys.argv)


# sudo apt-get install python3-bs4
# pip install python-dateutil