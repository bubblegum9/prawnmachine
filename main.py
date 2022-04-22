import json
from operator import sub
import praw
import requests as r
import os
from time import sleep

print(">Starting...")

webhook          = "https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay"
in_client_id     = "cFR01f6mWygnXN_3i6ZatQ"
in_client_secret = "ZeHWMXzZFei3YXPOnGRsJenPar0tHw"
in_user_agent    = "r/cat by u/LexCutter"

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

for submission in reddit.subreddit("cats").stream.submissions(skip_existing=True):
    print(">Got a Submission")
    if 'i.redd.it' in submission.url:
        print(">>its a picture")
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
        print(">>>posted")
        print(response)
    if submission.is_video == True:
        print(">>its a video")
        url_object = r.head(submission.url, allow_redirects=True)
        payload = {
            "content": str(url_object.url)
        }
        response = r.post(webhook, json = payload)
        print(">>>posted")
        print(response) 