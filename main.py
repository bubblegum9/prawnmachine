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
    'cats':         ['cats', catswebhook, delay]
#    'softwaregore': ['softwaregore', proxywebhook, delay],
#    'hardwaregore': ['hardwaregore', proxywebhook, delay],
#    'unixporn':     ['unixporn', proxyunixwebhook, delay]
}

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

print(">Connected!", "\n>Running Service...")


def reddit_thread(subreddit_name, webhook, delay):
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            #print("FLAIR TEXT", submission.link_flair_text)
            #print("IS OVER 18? ", submission.over_18, type(submission.over_18))

            print(subreddit_name, " >Got a Submission")
            print(subreddit_name, " > Checking if its not NSFW")
            if not submission.over_18 and not any(x in submission.title for x in ["#porn", "porn", "nsfw", "NSFW", "rescue", "What is this", "what is this", "doctor", "help", "consult", "advice"]):
                print(subreddit_name, " > NOT NSFW")
                print(subreddit_name, " > Checking if its a picture")
                if 'i.redd.it' in submission.url and "Cat Picture" in submission.link_flair_text:
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
                else:
                    print(subreddit_name, " > NOT a picture")
                    print(subreddit_name, " Was 'i.redd.it' in submission.url? ", 'i.redd.it' in submission.url)
                    print(subreddit_name, " Was 'Cat Picture' in submission.link_flair_text? ", "Cat Picture" in submission.link_flair_text)

                    print(subreddit_name, " > Checking if its a video")
                    if submission.is_video and "Video" in submission.link_flair_text:
                        print(subreddit_name," >>its a video")
                        url_object = r.head(submission.url, allow_redirects=True)
                        payload = {
                            "content": str(url_object.url)
                        }
                        response = r.post(webhook, json = payload)
                        print(subreddit_name," >>>posted")
                        print(response)
                    else:
                        print(subreddit_name, " > NOT a video")
                        print(subreddit_name, " Did submission.is_video evaluate to True? ", submission.is_video)
                        print(subreddit_name, " Was 'Video' in submission.link_flair_text? ", "Video" in submission.link_flair_text)

                print(subreddit_name, " > DONE\n\n\n")
                
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
