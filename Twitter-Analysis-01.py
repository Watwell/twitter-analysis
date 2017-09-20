import requests
from requests_oauthlib import OAuth1
import csv
import json
import os
from textblob import TextBlob
import sys

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\n',
    quoting = csv.QUOTE_MINIMAL)

# Sign up as a Twitter app developer and get auth keys
consumer_key = 'XXX_Fill_This_In_XXX'
consumer_secret = 'XXX_Fill_This_In_XXX'
access_token = 'XXX_Fill_This_In_XXX'
access_secret = 'XXX_Fill_This_In_XXX'

auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)

# TO RUN A FILE: exec(open("C:\\python\\GitHub\\Twitter-Analysis-01.py").read())

twitter_handle = 'some-twitter-handle'
excel_version = 20170919 #Date of run time

#*********** Maybe at trim_user=1 ****************

url_2 = 'https://api.twitter.com/1.1/search/tweets.json?q=' + twitter_handle + '&count=100'

res = requests.get(url_2, auth=auth)

tweets = res.json()

os.chdir('C:\\Python\\Twitter') #Update with the folder your file is in

excel_file_name = twitter_handle + '_tweets' + str(excel_version) +'.csv'
the_num = 0
finished_searching = 0

print(url_2)
print("Length: " + str(len(tweets['statuses'])))

with open(excel_file_name, 'w') as csvfile:
    thedatawriter = csv.writer(csvfile, dialect='mydialect')
    fieldnames = ['ID', 'Screen_Name', 'Created_at', 'Retweets', 'Favorites', 'Text', 'Sentiment', 'Month', 'Day', 'Year']
    thedatawriter.writerow(fieldnames)
    for i in range(1,16):
        print(i)
        for num, tweet in enumerate(tweets['statuses']):
            if(finished_searching == 0):
                t1 = tweet['id']
                t2 = tweet['user']['screen_name']
                t3 =  tweet['created_at']
                t4 =  tweet['retweet_count']
                t5 =  tweet['favorite_count']
                t6 =  tweet['text'].encode("utf-8", errors='ignore')
                t6a = t6.decode()
                tweet_text = TextBlob(t6a)
                t7 = tweet_text.sentiment.polarity
                array_row = [t1, t2, t3, t4, t5, t6a.encode("utf-8", errors='ignore'), t7]
                thedatawriter.writerow(array_row)
                the_num = num
        print(the_num)
        if(the_num < 99):
                finished_searching = 1
        if(finished_searching == 0):
            print(str(i) + ') ')
            print(t1)
            url_2 = 'https://api.twitter.com/1.1/search/tweets.json?q=' + twitter_handle + '&count=100&max_id=' + str(t1)
            print(url_2)
            res = requests.get(url_2, auth=auth)
            tweets = res.json()
