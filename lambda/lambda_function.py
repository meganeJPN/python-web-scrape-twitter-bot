#coding:utf-8

from requests_oauthlib import OAuth1Session
from webscrape import webscrape
import urllib3
import os

CK = os.environ['CK']
CS = os.environ['CS']
AT = os.environ['AT']
AS = os.environ['AS']

URL = 'https://api.twitter.com/1.1/statuses/update.json'

def lambda_handler(event, context):
    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    tweet = webscrape()
    print('## lambda_handler tweet')
    print(tweet)
    session = OAuth1Session(CK,CS,AT,AS)
    params = {"status":tweet}
    twitter = OAuth1Session(CK,CS,AT,AS)
    req = twitter.post(URL,params = params)
    
    if req.status_code == 200:
        return tweet
    else:
        return req.status_code