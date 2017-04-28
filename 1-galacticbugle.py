import urllib
import datetime as dt
from dateutil.tz import tzlocal
from pytz import timezone
import numpy as np


url = "http://export.arxiv.org/api/query?search_query=cat:(astro-ph.GA+OR+astro-ph.HE)+AND+abs:galactic+AND+lastUpdatedDate:[201305212000+TO+201309222000]&max_results=50&sortBy=submittedDate&sortOrder=descending"
data = urllib.urlopen(url).read()

print data

class Query_API(object):
    """
    Based on lazy-astroph: https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
    """

    def __init__(self, start_t, end_t):
        self.start_t = start_t
        self.end_t = end_t

        self.url_root = "http://export.arxiv.org/api/query?"
        self.sortby = "max_results=1&sortBy=submittedDate&sortOrder=descending" #  don't get more than 10 results for now

    #   Want to find all abstracts relating to Galactic astronomy, so have to search through all sub-categories for cross-listings

        self.astroph_subcat = ["GA", "CO", "EP", "HE", "IM", "SR"]

    def date_query(self):
        """
            Find the date range to query and create that part of the URL
        """
        daterange = "[{}2000+TO+{}2000]".format(self.start_t.strftime("%T%m%d"), self.end_t.strftime("%T%m%d"))
        query_range = "lastUpdatedDate:{}".format(daterange)
        return query_range

    def cat_query(self):
        """
        Heavily based on https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
        """
        #   build the query for the categories
        query_cat = "%28"
        for n, s in enumerate(self.astroph_subcat):
            query_cat+="astro-ph.{}".format(s)
            if n<len(self.astroph_subcat)-1:
                query_cat+="+OR+"
            else:
                query_cat+="%29"
        return query_cat + "+AND+abs:galactic+AND+"

    def create_url(self):
        """
        Create the full URL for the query
        """
        cat = self.cat_query()
        daterange = self.date_query()
        full_query = "search_query={}+AND+{}&{}".format(cat, daterange, self.sortby)
        return self.url_root+full_query

    def query_api(self):
        """
        Based on https://github.com/zingale/lazy-astroph/blob/master/lazy-astroph.py
        """
        api_response = urllib.urlopen(self.create_url()).read()
        
        return api_response

class Parse_Feed(object):


def bugle_search():
    """
    Actually do the search using the Query_API class
    """
    end_date = dt.date.today()
    query = Query_API(end_date - dt.timedelta(days=1), end_date)
    response = query.query_api()
    #   parse the responses
    return response


if __name__ == "__main__":
    print bugle_search()











