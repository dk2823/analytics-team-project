#!/usr/bin/python

from bs4 import BeautifulSoup
import requests, urllib.parse
import time


# Note - Have to get your "User-Agent" if you didn't set it up
#      - It looks like Google News web changes the class name often. Need to double check the class for div tag you want to grab before running this script
#      - 36 page is the last page.
#      - News feeds from https://www.google.com/search

def paginate(url, previous_url=None):
    # Break from infinite recursion
    if url == previous_url: return

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    from_date = "09/20/2019"
    to_date = "10/19/2019"

    keyword = "Amazon"

    params = {
        "q": f"{keyword}",
        "hl": "en",
        "tbas": "0",
        "tbs": f"cdr:1,cd_min:{from_date},cd_max:{to_date},sbd:1",
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
    yield from paginate(next_page_url, url)


def scrape():
    pages = paginate("https://www.google.com/search?")

    for soup in pages:
        print(f'Current page: {soup.select_one(".YyVfkd").text}')
        print()

        for data in soup.findAll('a', class_='WlydOe'): # <a> tag

            title = data.find('div', class_='mCBkyc JQe2Ld nDgy9d').text # div tag that has title
            link = data['href'] # a tag
            snippet = data.find('div', class_='GI74Re nDgy9d').text # div tag that has snippet
            published = data.find('p').find('span').text
            print(f'Title: {title}')
            print(f'Link: {link}')
            print(f'snippet: {snippet}')
            print(f'published: {published}')
            print()
            time.sleep(1)


scrape()