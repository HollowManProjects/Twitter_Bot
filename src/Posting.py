import tweepy
import os
import time
from datetime import datetime, date

# Posts based on user text (and optionally photo) input
def CreatePost(twitterAuth, message, media=[]):
    try:
        twitterAuth.update_status(message) if media==[] else twitterAuth.update_status(status=message, media_ids=media)
        print("Tweet posted")
    except tweepy.TweepError:
        print("Error occured while attempting to make post")
        return False
    return True

# Uploads media to Twitter to be used in post (4 photos || 1 video || 1 gif only)
def UploadMedia(twitterAuth,mediaFolder):
    ids=[]

    for media in os.listdir(mediaFolder):
        id = twitterAuth.media_upload("{}/{}".format(mediaFolder,media))
        ids.append(id.media_id)

    return ids

# Formats the message based on
def CreateMessage(PostTextFile, HashtagFile):
    message = ""

    # Get main message data
    with open(PostTextFile, "r") as text:
        message += text.read()

    # Grab remaining hashtags
    with open(HashtagFile, "r") as text:
        tags = text.read().splitlines()
    
    # Append as many hashtags with remaining text
    for tag in tags:
        if len("{} {}".format(message,tag)) < 280:
            message += " {}".format(tag)
        else:
            break

    return message


# Check if we posted in today
def CheckLastPost(lastCheckFile, postMessageFile):

    with open(lastCheckFile, "r") as check:
        lastPostTime = datetime.strptime(check.read().strip(), "%Y-%m-%d %H:%M:%S.%f")

        # Get post message last mod time
        modTime = os.path.getmtime(postMessageFile)
        lastModTimeStr = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTime))
        lastModeTime = datetime.strptime(lastModTimeStr, "%Y-%m-%d %H:%M:%S")

        print(lastModeTime)
        print(lastPostTime)
        if lastPostTime.date() == date.today() or lastModeTime <= lastPostTime:
            return False

    return True    

# Update to mark this as the most recent post
def UpdateLastPost(lastCheckFile):  
    with open(lastCheckFile, "w") as lastFile:
        lastFile.write(str(datetime.now()))
