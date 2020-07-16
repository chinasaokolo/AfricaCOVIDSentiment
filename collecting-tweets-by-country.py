#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Twitter/Github: @buildwithcycy
"""
TO-DO
Searching for tweets based of country
"""

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import pandas as pd
import json
import csv
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

#Add your credentials here
twitter_keys = {
        'consumer_key':        'yourkeygoesbetweenthesequotes',
        'consumer_secret':     'yourkeygoesbetweenthesequotes',
        'access_token_key':    'yourkeygoesbetweenthesequotes',
        'access_token_secret': 'yourkeygoesbetweenthesequotes'
    }

#Setup access to API
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tweepy.API(auth)

#Making call to perform a search by country
#Places are named locations with corresponding geo coordinates.
places = api.geo_search(query="NIGERIA", granularity="country") 
place_id = places[0].id

tweets = api.search(q="place:%s" % place_id,  count=1000)
for tweet in tweets:
    print (tweet.text , " | " , tweet.place.name if tweet.place else "Undefined place")
