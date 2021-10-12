#!/usr/bin/python

import sys
from pygooglenews import GoogleNews
import time


# when variable should accept only "{d}[1-24]h", "{d}[1-365]d", "{d}[1-48]m"
# from_ and to_ variables should be %Y-%m-%d format. (ex) 2020-07-01
# news feeds from https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en

def get_titles_links(keyword, when = None, from_ = None, to_ = None):
    # Assumes we need US news only
    gn = GoogleNews(lang='en', country='US')

    if when == None and from_ == None and to_ == None:
        return getStories(gn.search(keyword))
    elif when != None and from_ == None and to_ == None:
        return getStories(gn.search(keyword, when))
    else:
        return getStories(gn.search(keyword, from_, to_))



def getStories(items):
    stories = []
    newsItems = items['entries']

    for each in newsItems:
        story = {
            'title': each.title,
            'link' : each.link,
            'published' : each.published
        }
        stories.append(story)
        print(f'Title: {each.title}')
        print(f'Link: {each.link}')
        print(f'Published: {each.published}')
        print()

        time.sleep(1)

    return stories

def main(argv):
    if len(sys.argv) < 2:
        print("Please provide keyword/time.")
        sys.exit()
    else :
        if len(sys.argv) == 2 : # only keyword
            get_titles_links(argv[1])
        elif len(sys.argv) == 3: # when exists
            get_titles_links(argv[1], argv[2])
        else: # keyword with from_ and to_
            get_titles_links(argv[1], argv[2], argv[3])


if __name__ == "__main__":
    main(sys.argv)


