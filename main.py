import json
from operator import sub
import praw
import requests as r
import os
from dotenv import load_dotenv
from time import sleep

load_dotenv()
webhook          = os.getenv('WEBHOOK')
in_client_id     = os.getenv('CLIENT_ID')
in_client_secret = os.getenv('CLIENT_SECRET')
in_user_agent    = os.getenv('USER_AGENT')

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

for submission in reddit.subreddit("cats").stream.submissions(skip_existing=True):
    if 'i.redd.it' in submission.url:
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
        print(response)
    if submission.is_video == True:
        url_object = r.head(submission.url, allow_redirects=True)
        payload = {
            "content": str(url_object.url)
        }
        response = r.post(webhook, json = payload)
        print(response) 