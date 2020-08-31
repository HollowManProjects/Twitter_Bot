#!/usr/bin/python3
import tweepy
from time import sleep
import random
import os

print("Starting Twitter Follow and Like")

# List file paths
twitterData = "/Users/tim_drake/Documents/Personal/Etc/TwitterBot/twitterLogin.txt"
hashtagFile = "/Users/tim_drake/Documents/Personal/Etc/TwitterBot/twitterHashtags.txt"

# Setup Twitter object
with open(twitterData) as file:
    data = file.read().splitlines()

auth = tweepy.OAuthHandler(data[0], data[1])
auth.set_access_token(data[2], data[3])
api = tweepy.API(auth)

try:
    api.verify_credentials()
except:
    print("Couldn't log in to Twitter")
    exit(0)

# Get hashtags
tags = ""
with open(hashtagFile, "r") as text:
    tags = text.read().splitlines()

likeCount = 0
followCount = 0
for x in range(5):

    # Pick random tag
    randomTag = random.choice(tags)
    tags.remove(randomTag)

    # Get tweets
    for tweet in tweepy.Cursor(api.search, q=randomTag, count=10).items():
        
        # Likes post, if we haven't already
        if not tweet.favorited:
            try:
                tweet.favorite()
                likeCount += 1
            except Exception as e:
                print("Already liked this post")

        # Randomized to follow, if aren't already
        if random.choice([True, False]) and not tweet.user.following:
            tweet.user.follow()
            followCount += 1

        sleep(1)


print("Finished liking {} tweets and following {} new users".format(likeCount, followCount))