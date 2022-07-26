import praw
import requests as r
import os
from time import sleep
import threading

print(">Starting...")

catswebhook      = "https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay"
proxywebhook     = "https://discord.com/api/webhooks/892342475681853460/eq6jJOvtUxu4JBE3AWg4nkBo0rWTpWDPWSuM-j7tZtYix1PqhxNEE4WgP6s9SQrELoGH"
proxyunixwebhook = "https://discord.com/api/webhooks/993542686122459186/n4xl7dSajgH9YOtO6VmOQy5HSLtCktDSnSGMLrJHzyDejX1M925FAcFiFe5PwgQ5F1ax"
in_client_id     = "cFR01f6mWygnXN_3i6ZatQ"
in_client_secret = "ZeHWMXzZFei3YXPOnGRsJenPar0tHw"
in_user_agent    = "r/cat by u/LexCutter"
delay = 0

subreddit_list = {
    'cats':         ['cats', catswebhook, delay],
    'softwaregore': ['softwaregore', proxywebhook, delay],
    'hardwaregore': ['hardwaregore', proxywebhook, delay],
    'unixporn':     ['unixporn', proxyunixwebhook, delay]
}

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

print(">Connected!", "\n", ">Running Service...")


def reddit_thread(subreddit_name, webhook, delay):
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            if(submission.link_flair_text != None):
                print(submission.link_flair_text)
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

def main():
    while(True):
        sleep(1)

if __name__=='__main__':
    thread_list = list()

    for index, subreddit in enumerate(subreddit_list):
        arguments = [
            subreddit_list[subreddit][0],
            subreddit_list[subreddit][1],
            subreddit_list[subreddit][2]
        ]
        thread_list.append(
            threading.Thread(target=reddit_thread, args = arguments, daemon=True)
        )
        thread_list[index].start()
    main()
