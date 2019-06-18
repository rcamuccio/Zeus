# !/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Richard Camuccio
# 18 Jun 2019
#
# Last update: 18 Jun 2019
#
# Zeus - Weather alert system bot
#

from twython import Twython

consumer_key = 
consumer_secret = 
access_token = 
access_token_secret = 

twitter = Twython(consumer_key, consumer_secret, access_token, access_token_secret)

message = "Hello world!"
twitter.update_status(status=message)
print("Tweeted: %s" % message)