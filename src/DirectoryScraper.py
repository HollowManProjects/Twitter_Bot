#!/usr/bin/python3
import tweepy
import Posting
from time import sleep
import os

print("Starting Twitter Posting")

# List file paths
twitterData = "/Users/tim_drake/Documents/Personal/Etc/TwitterBot/twitterLogin.txt"
SubFolderPath = "/Users/tim_drake/Documents/Projects/Twitter_Bot/src/Test_Sub_Folder"

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

# Scrap SubFolderDirectory for posting folders
for subFolder in os.listdir(SubFolderPath):

    # Check for files
    lastPost = "{}/{}/{}".format(SubFolderPath, subFolder, "lastPost.txt")
    postMessage = "{}/{}/{}".format(SubFolderPath, subFolder, "postMessage.txt")
    hashtags = "{}/{}/{}".format(SubFolderPath, subFolder, "hashtags.txt")
    mediaFolder = "{}/{}/{}".format(SubFolderPath, subFolder, "Media")    

    if not os.path.exists(lastPost) or not os.path.exists(postMessage) or not os.path.exists(hashtags) or not os.path.exists(mediaFolder):
        print("Not all necessary files are present in this directory!\n")
        continue
    
    # Check for latest post / if postMessage has been modified since last post
    if not Posting.CheckLastPost(lastPost, postMessage):
        print("Nothing new to post or has already posted in the last 24 hours!\n")
        continue

    # Create message
    message = Posting.CreateMessage(postMessage,hashtags)

    # Grab media
    mediaIds = Posting.UploadMedia(api, mediaFolder)
    
    # Post
    if Posting.CreatePost(api,message,mediaIds):

        # Update latest post file
        Posting.UpdateLastPost(lastPost)

    print("Finished Twitter Posts")