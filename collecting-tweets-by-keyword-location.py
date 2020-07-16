#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Twitter/Github: @buildwithcycy
"""
Sentiment Analysis on Covid19 Tweets (Africa) 


#####################################################################
DATASET
#####################################################################
Our data consists of a set of tweets collected using the 
Tweepy Library around the hashtags



#####################################################################
PROJECT MOTIVATION: Exploring Sentiment towards covid19 across Africa
#####################################################################
The proliferation of fake news and misinformation has been a con-
stant battle for health officials and policy makers as they work to 
curb the spread of COVID-19 in Africa. Our goal is to explore techniques that 
the AI community can offer to help address this issue.
"""

import tweepy #opensource Python library for accessing the Twitter API
import datetime
import json
import csv
import pandas as pd

#####################################################################
# STEP 1: Adding your credentials
# Refer to credentials provided in Twitter developper account under
# app
#####################################################################
twitter_keys = {
        'consumer_key':        'yourkeygoesbetweenthesequotes',
        'consumer_secret':     'yourkeygoesbetweenthesequotes',
        'access_token_key':    'yourkeygoesbetweenthesequotes',
        'access_token_secret': 'yourkeygoesbetweenthesequotes'

    }

#Setting up access to API using your credentials
auth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])
auth.set_access_token(twitter_keys['access_token_key'], twitter_keys['access_token_secret'])

api = tweepy.API(auth)

#####################################################################
# STEP 2: EXAMPLE 1 - TESTING YOUR ACCESS TO API
#         Displays your home timeline tweets in real-time
#####################################################################

"""
#Making call to Twitter api
public_tweets = api.home_timeline()

#Prints each tweet as it appears on your home timeline
for tweet in public_tweets:
    print(tweet.text + "\n")


#Gets the most recent tweet from your timeline and saves it as status
status = public_tweets[0]

#Converts tweet to a string
json_str = json.dumps(status._json)

#Deserialise string into python object
parsed = json.loads(json_str)

#Prints the tweet as a Json object 
#Use this statement to view the attributes and structure of a tweet 
print(json.dumps(parsed, indent=4, sort_keys=True))
"""

#####################################################################
# STEP 3: EXAMPLE 2 - DOWNLOADING ALL TWEETS OF A USER IN A CSV FILE
#####################################################################
"""
def get_all_tweets_from_user(screen_name):
  
  #Gets all the tweets from a user and saves them in a CSV file  
  
  # initialize a list to hold all the Tweets
  alltweets = []
  
  # make initial request for most recent tweets 
  # (200 is the maximum allowed count)
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
 
  # save most recent tweets
  alltweets.extend(new_tweets)
  
  # save the id of the oldest tweet less one to avoid duplication
  oldest = alltweets[-1].id - 1
  
  # keep grabbing tweets until there are no tweets left
  while len(new_tweets) > 0:
    print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % (len(alltweets)))
    ### END OF WHILE LOOP ###
  
    # transform the tweepy tweets into a 2D array that will populate the csv
  outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count,
  tweet.in_reply_to_screen_name, tweet.retweeted] for tweet in alltweets]
  
  print ("done")
  return outtweets

#Practical example on the tweets of WHO
screen_name = 'WHO'  #specify the username without the @
out_tweets = get_all_tweets_from_user (screen_name)

#Creates a new CSV file if one doesn't exist
#If a CSV file exists, then the contents of the existing file are overwritten
with open('dataset-' + '%s-tweets.csv' % screen_name, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","text","likes","in reply to","retweeted"])
    writer.writerows(out_tweets) #writes the tweets to the CSV file
pass
"""


#####################################################################
# STEP 4: EXAMPLE 3 - DOWNLOADING TWEETS BASED ON SPECIFIC CRITERIA
# Here we will download tweets based of a keyword and location
# Unfortunately, Twitter only allows to pull tweets within a week
# Older tweets can be pulled using other scraping methods
#####################################################################

#Open/Create a file to append data
#Creates a new CSV file if one doesn't exist under that name
#If a CSV file exists, then the new tweets are added to the bottom of the CSV
csvFile = open('covid19-tweets-africa-southafrica-wellignton.csv', 'a')

#Use csv Writer
csvWriter = csv.writer(csvFile)

###############
# SEARCH CRITERIA
#
#keyword = can be hashtag
#geocode = (latitude, longitude, radius). We search tweets that are located 
#within a circle from with center as (latitude, longitude). For baseline case,
#I picked Wellington, a city located near Cape Town to maximize the amount of 
#tweets
#language = english
#since and until.Discovered later that these options are for paid version.
#items = the maximum number of tweets to pull

# TO-DO: searching with multiple keywords, searching based on country.
###############

for tweet_info in tweepy.Cursor(api.search,q="corona",
                           count=100,  
                           geocode="-33.644236,19.010579,1000km",
                           lang="en", 
                           #tweet_mode="extended",
                            since="2020-06-02",
                            until ="2020-06-09").items(10):
    
    retweeted_value = False #To keep track of a wether this a retweet
    if 'retweeted_status' in dir(tweet_info):
        #Discard retweets (suggestions welcome)
        try:
            tweet = 'RT-'+tweet_info.retweeted_status.extended_tweet["full_text"]
            retweeted_value = True
        except AttributeError:
            tweet ='RT-'+tweet_info.retweeted_status.text
            retweeted_value = True
    else:
        #Keep original tweets
        #There's definitely a better way to do this 
        try:
            tweet = tweet_info.extended_tweet["full_text"]
            print (tweet_info.created_at, tweet, tweet_info.favorite_count, tweet_info.retweeted, tweet_info.retweet_count, tweet_info.user.verified,tweet_info.coordinates,tweet_info.user.location, "\n")
            csvWriter.writerow([tweet_info.created_at, tweet.encode('utf-8'), tweet_info.favorite_count,  retweeted_value, tweet_info.retweet_count,  tweet_info.user.verified,tweet_info.coordinates, tweet_info.user.location.encode('utf-8')])
            
        except AttributeError:
            tweet = tweet_info.text
            print (tweet_info.created_at, tweet, tweet_info.favorite_count, tweet_info.retweeted, tweet_info.retweet_count, tweet_info.user.verified,tweet_info.coordinates,tweet_info.user.location, "\n")
            csvWriter.writerow([tweet_info.created_at, tweet.encode('utf-8'), tweet_info.favorite_count,  retweeted_value, tweet_info.retweet_count,  tweet_info.user.verified,tweet_info.coordinates, tweet_info.user.location.encode('utf-8')])
    
    #print (tweet_info.created_at, tweet, tweet_info.favorite_count, tweet_info.retweeted, tweet_info.retweet_count, tweet_info.user.verified,tweet_info.coordinates,tweet_info.user.location, "\n")
    #csvWriter.writerow([tweet_info.created_at, tweet, tweet_info.favorite_count,  retweeted_value, tweet_info.retweet_count,  tweet_info.user.verified,tweet_info.coordinates, tweet_info.user.location.encode('utf-8')])
    #convert to string
    #json_str = json.dumps(tweet_info._json)
    print ("done")
    
csvFile.close() #close the csvFile
