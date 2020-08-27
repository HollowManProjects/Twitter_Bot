import tweepy
from time import sleep
from datetime import datetime, date
from github import Github, Repository, Commit

""" Checks all repos commits since the lastCheck, if any are founds then they are posted """
def PostNewCommits(repos = any, twitterApi = any, githubAccount = any, lastCheck = any):
    for repoName in repos:
        repo = githubAccount.get_repo(repoName)
        makeTweet = False

        # Makes message
        message = "{} Update(s):\n".format(repo.name)

        for commit in repo.get_commits(since=lastCheck):
            makeTweet = True
            message += "* {}\n".format(commit.commit.message)

        if len(message) >= 280:
            message = message[0:277] + "..."

        # Makes tweet if needed
        if makeTweet == True:
            try:
                twitterApi.update_status(message)
                print(message)
            except tweepy.TweepError:
                print("Error")
                pass
