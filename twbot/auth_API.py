import tweepy
from django.conf import settings

def get_auth_API():
    consumer_key=settings.API_KEY
    consumer_secret=settings.API_KEY_SECRET
    access_token=settings.ACCESS_TOKEN
    access_token_secret=settings.ACCESS_TOKEN_SECRET

    auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_token,access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)
    return api
