from concurrent.futures import thread
import json
from operator import sub
from weakref import proxy
import praw
import requests as r
import os
from time import sleep
import threading

print(">Starting...")


catswebhook      = "https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay"
proxywebhook     = "https://discord.com/api/webhooks/892342475681853460/eq6jJOvtUxu4JBE3AWg4nkBo0rWTpWDPWSuM-j7tZtYix1PqhxNEE4WgP6s9SQrELoGH"
in_client_id     = "cFR01f6mWygnXN_3i6ZatQ"
in_client_secret = "ZeHWMXzZFei3YXPOnGRsJenPar0tHw"
in_user_agent    = "r/cat by u/LexCutter"
delay = 5

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

def cats():
    subreddit_name = "cats"
    webhook = catswebhook
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            print(subreddit_name," >Got a Submission")
            if 'i.redd.it' in submission.url:
                print(subreddit_name," >>its a picture")
                payload = {
                    "content": None,
                    "embeds": [
                        {
                            "title": str(submission.title),
                            "description": None,
                            "color":356357,
                            "image":{
                                "url":str(submission.url)
                            }
                        }
                    ]
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            if submission.is_video == True:
                print(subreddit_name," >>its a video")
                url_object = r.head(submission.url, allow_redirects=True)
                payload = {
                    "content": str(url_object.url)
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            sleep(delay)
    except Exception as e:
        print('Error in ', subreddit_name, ': ', e)
        pass

def softwaregore():
    subreddit_name = "softwaregore"
    webhook = proxywebhook
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            print(subreddit_name, " >Got a Submission")
            if 'i.redd.it' in submission.url:
                print(subreddit_name, " >>its a picture")
                payload = {
                    "content": None,
                    "embeds": [
                        {
                            "title": str(submission.title),
                            "description": None,
                            "color":356357,
                            "image":{
                                "url":str(submission.url)
                            }
                        }
                    ]
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            if submission.is_video == True:
                print(subreddit_name," >>its a video")
                url_object = r.head(submission.url, allow_redirects=True)
                payload = {
                    "content": str(url_object.url)
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            sleep(delay)
    except Exception as e:
        print('Error in ', subreddit_name, ': ', e)
        pass

def hardwaregore():
    subreddit_name = "hardwaregore"
    webhook = proxywebhook
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            print(subreddit_name," >Got a Submission")
            if 'i.redd.it' in submission.url:
                print(subreddit_name," >>its a picture")
                payload = {
                    "content": None,
                    "embeds": [
                        {
                            "title": str(submission.title),
                            "description": None,
                            "color":356357,
                            "image":{
                                "url":str(submission.url)
                            }
                        }
                    ]
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            if submission.is_video == True:
                print(subreddit_name," >>its a video")
                url_object = r.head(submission.url, allow_redirects=True)
                payload = {
                    "content": str(url_object.url)
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            sleep(delay)
    except Exception as e:
        print('Error in ', subreddit_name, ': ', e)
        pass

def unixporn():
    subreddit_name = "unixporn"
    webhook = proxywebhook
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            print(subreddit_name," >Got a Submission")
            if 'i.redd.it' in submission.url:
                print(subreddit_name," >>its a picture")
                payload = {
                    "content": None,
                    "embeds": [
                        {
                            "title": str(submission.title),
                            "description": None,
                            "color":356357,
                            "image":{
                                "url":str(submission.url)
                            }
                        }
                    ]
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            if submission.is_video == True:
                print(subreddit_name," >>its a video")
                url_object = r.head(submission.url, allow_redirects=True)
                payload = {
                    "content": str(url_object.url)
                }
                response = r.post(webhook, json = payload)
                print(subreddit_name," >>>posted")
                print(response)
            sleep(delay)
    except Exception as e:
        print('Error in ', subreddit_name, ': ', e)
        pass

thread_cats         = threading.Thread(target=cats, daemon=True)
thread_hardwaregore = threading.Thread(target=hardwaregore, daemon=True)
thread_softwaregore = threading.Thread(target=softwaregore, daemon=True)
thread_unixporn     = threading.Thread(target=unixporn, daemon=True)

thread_cats.start()
thread_hardwaregore.start()
thread_softwaregore.start()
thread_unixporn.start()
