"""
    This program uses an API querier based on lazy-astroph (https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py) and a feed parser based on https://github.com/zonca/python-parse-arxiv/blob/master/python_arXiv_parsing_example.py
    
    Contact Fiona H. Panther (Australian National University) for more information:
        fiona.panther@anu.edu.au
        @fipanther on Twitter
        @fipanther on GitHub
"""
from __future__ import print_function
import urllib
import datetime as dt
import feedparser
import tweepy
from secrets import *

#   I run this program daily as a cronjob with a Miniconda python2.7 install on a CentOS 7.2 machine. If you want to run the program, you will need to install the feedparser and tweepy modules (pip install feedparser and pip install tweepy work fine). If you want it to tweet, you will also need to create your own twitter bot account, and a developer account. From the developer acct, you can obtain access keys. These go in to the secrets file. Obviously, the secrets file is not included here so you can't get access to the Galactic Bugle bot. You can modify the main portion of this file to simply obtain and parse an atom feed from arXiv

class Query_API(object):
    """
    Based on lazy-astroph: https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
    """

    def __init__(self, start_t, end_t):
        self.start_t = start_t
        self.end_t = end_t

        self.url_root = "http://export.arxiv.org/api/query?"
        #   if you want to change the number of results returned by the querier, change the number in this string
        self.sortby = "max_results=50&sortBy=submittedDate&sortOrder=descending"
        self.astroph_subcat = ["GA", "CO", "EP", "HE", "IM", "SR"]

    def date_query(self):
        """
            Find the date range to query and create that part of the URL
        """
        daterange = "[{}2000+TO+{}2000]".format(self.start_t.strftime("%Y%m%d"), self.end_t.strftime("%Y%m%d"))
        query_range = "lastUpdatedDate:{}".format(daterange)
        return query_range

    def cat_query(self):
        """
        Heavily based on https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
        """
        query_cat = "("
        for n, s in enumerate(self.astroph_subcat):
            query_cat+=r"astro-ph.{}".format(s)
            if n<len(self.astroph_subcat)-1:
                query_cat+=r"+OR+"
            else:
                query_cat+=")"
        #   Changing the keyword here (Galactic) to your chosen keyword will yield abstracts with that word in them (this is a confusing sentence)
        return "cat:" + query_cat + r"+AND+abs:Galactic"

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
    #   Access the authentication keys from the secrets file
    auth = tweepy.auth.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)
    for i in tweets:
        #  send them to the bot for tweeting
        twitter_api.update_status(i)

















