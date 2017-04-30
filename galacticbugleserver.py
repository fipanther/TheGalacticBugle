from __future__ import print_function
import urllib
import datetime as dt
import feedparser
import tweepy
from tweepy.auth import OAuthHandler
from secrets import *

class Query_API(object):
    def __init__(self, start_t, end_t):
        self.start_t = start_t
        self.end_t = end_t
        
        self.url_root = "http://export.arxiv.org/api/query?"
        self.sortby = "max_results=50&sortBy=submittedDate&sortOrder=descending"
        self.astroph_subcat = ["GA", "CO", "EP", "HE", "IM", "SR"]
    
    def date_query(self):
        daterange = "[{}2000+TO+{}2000]".format(self.start_t.strftime("%Y%m%d"), self.end_t.strftime("%Y%m%d"))
        query_range = "lastUpdatedDate:{}".format(daterange)
        return query_range
    
    def cat_query(self):
        query_cat = "("
        for n, s in enumerate(self.astroph_subcat):
            query_cat+=r"astro-ph.{}".format(s)
            if n<len(self.astroph_subcat)-1:
                query_cat+=r"+OR+"
            else:
                query_cat+=")"
        
        return "cat:" + query_cat + r"+AND+abs:Galactic"

    def create_url(self):
        cat = self.cat_query()
        daterange = self.date_query()
        full_query = r"search_query={}+AND+{}&{}".format(cat, daterange, self.sortby)
        return self.url_root+full_query

    def query_api(self):
        api_response = urllib.urlopen(self.create_url()).read()
        return api_response


def bugle_search():
    end_date = dt.date.today()
    query = Query_API(end_date - dt.timedelta(days=3), end_date - dt.timedelta(days=2))
    response = query.query_api()
    return response

def bugle_tweet(api_response):
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
    
    auth = tweepy.auth.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    twitter_api = tweepy.API(auth)
    twitter_api.update_status('server test please ignore')
#    for i in tweets:
#        #  send them to the bot for tweeting
#        twitter_api.update_status(i)

















