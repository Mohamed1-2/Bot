from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(TweetkeyWords)
admin.site.register(TweetunimportantwWord)
admin.site.register(Tweetgeotag)
admin.site.register(DirectMessage)

