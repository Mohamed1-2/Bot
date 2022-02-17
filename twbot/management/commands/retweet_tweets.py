from django.core.management.base import BaseCommand

import tweepy

from twbot.models import TweetkeyWords,TweetunimportantwWord,Tweetgeotag
from twbot.auth_API import get_auth_API

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.api= get_auth_API

        self.unwanterWords=list(TweetunimportantwWord.objects.values_list('k_word',flat=True))
        super(MyStreamListener,self).__init__()
    def on_connect(self):
        print("Successfully Connected To Twitter API")
    def on_status(self,tweet):
        tweet_id = tweet.id

        if tweet.truncated:
            tweet_text = tweet.extended_tweet["full_text"]
        else:
            tweet_text = tweet.text
        if not hasattr(tweet, "retweeted_status"):
            for unwanterWord in self.unwanterWords:
                if unwanterWord in tweet_text :
                    break
                else :
                    api = get_auth_API()
                    resp= api.retweet(tweet_id)

                    print(tweet_id)

    def on_error(self,status_code):
        if status_code==420:
            return False
class Command(BaseCommand):
    def handle(self,*args ,**kwargs):
        try :
            filterWords=TweetkeyWords.objects.values_list('k_word',flat=True )
            filterWords_join=','.join(filterWords)
            filterGeo=Tweetgeotag.objects.values_list('value',flat=True)
            filterGeo=[float(cor)for geo in filterGeo for cor in geo.split(',')]
            api=get_auth_API()
            stream_listener= MyStreamListener()
            stream= tweepy.Stream(auth=api.auth ,listener=stream_listener, tweet_mode='extended')
            stream.filter(track=[filterWords_join],locations=filterGeo)
        except Exception as e:
            print(e)
