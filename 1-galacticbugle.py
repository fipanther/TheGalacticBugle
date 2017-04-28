"""
    This program uses an API querier based on lazy-astroph (https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py) and a feed parser based on https://github.com/zonca/python-parse-arxiv/blob/master/python_arXiv_parsing_example.py
"""

from __future__ import print_function
import urllib
import datetime as dt
from dateutil.tz import tzlocal
from pytz import timezone
import numpy as np
import feedparser

class Query_API(object):
    """
    Based on lazy-astroph: https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
    """

    def __init__(self, start_t, end_t):
        self.start_t = start_t
        self.end_t = end_t

        self.url_root = "http://export.arxiv.org/api/query?"
        self.sortby = "max_results=50&sortBy=submittedDate&sortOrder=descending" #  don't get more than 10 results for now

    #   Want to find all abstracts relating to Galactic astronomy, so have to search through all sub-categories for cross-listings

        self.astroph_subcat = ["GA", "CO", "EP", "HE", "IM", "SR"]

    def date_query(self):
        """
            Find the date range to query and create that part of the URL
        """
        daterange = "[{}2000+TO+{}2000]".format(self.start_t.strftime("%Y%m%d"), self.end_t.strftime("%Y%m%d"))
        query_range = "lastUpdatedDate:{}".format(daterange)
        #print('QUERY RANGE =', query_range)
        return query_range

    def cat_query(self):
        """
        Heavily based on https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
        """
        #   build the query for the categories
        query_cat = "("
        for n, s in enumerate(self.astroph_subcat):
            query_cat+=r"astro-ph.{}".format(s)
            if n<len(self.astroph_subcat)-1:
                query_cat+=r"+OR+"
            else:
                query_cat+=")"
  
        return "cat:" + query_cat + r"+AND+abs:galactic"

    def create_url(self):
        """
        Create the full URL for the query
        """
        cat = self.cat_query()
        daterange = self.date_query()
        full_query = r"search_query={}+AND+{}&{}".format(cat, daterange, self.sortby)
        return self.url_root+full_query

    def query_api(self):
        """
        Based on https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
        """
        api_response = urllib.urlopen(self.create_url()).read()
        
        return api_response


def bugle_search():
    """
    Actually do the search using the Query_API class
    """
    end_date = dt.date.today()
    query = Query_API(end_date - dt.timedelta(days=3), end_date - dt.timedelta(days=2))
    response = query.query_api()
    #   parse the responses
    return response

def bugle_tweet(api_response):
    """
        Takes the api response and parses it into tweets, a simple variation on https://github.com/zonca/python-parse-arxiv/blob/master/python_arXiv_parsing_example.py
    """
    feed = feedparser.parse(api_response)
    tweet_list = []
    for entry in feed.entries:
        #   Make the tweet!
        tweet_root = 'https://arxiv.org/abs/'+str(entry.id.split('/abs/')[-1])
        tweet_root_len = len(tweet_root)
        remaining_len = 140-tweet_root_len
        tweet_title = entry.title[0:remaining_len]
        tweet_out = tweet_title + ' ' + tweet_root
        tweet_list.append(tweet_out)
    
    return tweet_list


if __name__ == "__main__":
    api_response = bugle_search()
    tweets = bugle_tweet(api_response)
    for i in tweets:
        #   send them to the bot for tweeting
        print(i)

















