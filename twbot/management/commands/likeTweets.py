from django.core.management.base import BaseCommand

import tweepy

from twbot.models import TweetkeyWords,TweetunimportantwWord,Tweetgeotag

from twbot.auth_API import get_auth_API

class MyStreamListener(tweepy.StreamListener):
    def __init__(self):
        self.unwanterWords=list(TweetunimportantwWord.objects.values_list('k_word',flat=True))

        super(MyStreamListener,self).__init__()
    def on_connect(self):

        print("Successfully Connected To Twitter API")
    def on_status(self,status):
        tweet_id = status.id

        if status.truncated:
            tweet_text = status.extended_tweet["full_text"]
        else:
            tweet_text = status.text
        if not hasattr(status, "retweeted_status"):
            for unwanterWord in self.unwanterWords:
                if unwanterWord in tweet_text :
                    break
                else :
                    api = get_auth_API()
                    resp= api.create_favorite(tweet_id)
                    print(tweet_id)
    def on_error(self,status_code):

        if status_code==420:

            return False

class Command(BaseCommand):
    def handle(self,*args ,**kwargs):
        try :
            filter_Words=TweetkeyWords.objects.values_list('k_word',flat=True )
            filter_Words=','.join(filter_Words)
            filter_location=Tweetgeotag.objects.values_list('value',flat=True)
            filter_location=[float(cor)for loc in filter_location for cor in loc.split(',')]
            api=get_auth_API()
            stream_listener= MyStreamListener()
            stream= tweepy.Stream(auth=api.auth ,listener=stream_listener, tweet_mode='extended')
            stream.filter(track=[filter_Words],locations=filter_location)
        except Exception as e:
            print(e)


