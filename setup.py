#!/usr/bin/python3
import tweepy
import methodDef
from time import sleep
from datetime import datetime, date
from github import Github, Repository, Commit

# Set file paths
twitterData = "/home/superboy/Documents/Personal/Etc/twitterData.txt"
lastCheckFile = "/home/superboy/Documents/Projects/TwitterBot/lastCheck.txt"
repoChecklist = "/home/superboy/Documents/Projects/TwitterBot/repoChecklist.txt"

# Check if we posted in today
with open(lastCheckFile, "r") as file:
    lastCheck = datetime.strptime(file.read().strip(), "%Y-%m-%d %H:%M:%S.%f")

    if lastCheck.date() == date.today():
        exit(0)

# Get login creditials
with open(twitterData) as file:
    data = file.read().splitlines()

auth = tweepy.OAuthHandler(data[0], data[1])
auth.set_access_token(data[2], data[3])
api = tweepy.API(auth)

# Verify credentials
try:
    api.verify_credentials()
except:
    print("Couldn't log in to Twitter")
    exit(0)

# Logins into Github with token
account = Github(str(data[4]))

# Grab repo list
with open(repoChecklist, "r") as checklist:
    repos = checklist.read().split()

# Posts project updates
methodDef.PostNewCommits(repos, api, account, lastCheck)
print("Finished")

# Update to mark this as the most recent post
with open(lastCheckFile, "w") as lastFile:
    lastFile.write(str(datetime.now()))
