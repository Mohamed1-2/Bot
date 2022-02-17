from django.core.management.base import BaseCommand

import tweepy

from twbot.models import  DirectMessage,latestFollowers

from twbot.auth_API import get_auth_API

class Command(BaseCommand):
    def handle(self,*args ,**kwargs):
        try :
            api =get_auth_API()
            latestFollower_id = latestFollowers.objects.get().latestFollower_id
            message=DirectMessage.objects.get().message

            for follower in api.followers_ids():
                if follower==latestFollower_id:
                    break
                else:
                    api.send_direct_message(follower,message)
        except latestFollowers.DoesNotExist:
            api=get_auth_API()
            last_Follower_id =api.followers_ids()[0]

            latestFollowers.objects.create(latestFollower_id=last_Follower_id)
        except Exception as e :
            print(e)


