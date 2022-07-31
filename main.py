# __________                                _____                .__    .__               
# \______   \____________ __  _  ______    /     \ _____    ____ |  |__ |__| ____   ____  
#  |     ___/\_  __ \__  \\ \/ \/ /    \  /  \ /  \\__  \ _/ ___\|  |  \|  |/    \_/ __ \ 
#  |    |     |  | \// __ \\     /   |  \/    Y    \/ __ \\  \___|   Y  \  |   |  \  ___/ 
#  |____|     |__|  (____  /\/\_/|___|  /\____|__  (____  /\___  >___|  /__|___|  /\___  >
#                        \/           \/         \/     \/     \/     \/        \/     \/ 
# PrawnMachine
# https://github.com/crackMaker/redditcatz
# A (mostly) smart reddit scraper to discord webhook

import sys
try:
    import functools
    from termcolor import colored
    import praw
    import requests as r
    import os
    from time import sleep
    import threading
    import random
except Exception as e:
    print(e, "\n")
    sys.exit("Error while trying to import required libraries (did you install the dependencies?)")

print = functools.partial(print, flush=True)

random.seed()

print(">Starting...")

catswebhook      = "https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay"
proxywebhook     = "https://discord.com/api/webhooks/892342475681853460/eq6jJOvtUxu4JBE3AWg4nkBo0rWTpWDPWSuM-j7tZtYix1PqhxNEE4WgP6s9SQrELoGH"
proxyunixwebhook = "https://discord.com/api/webhooks/1002975870333501540/UrNjNuJjrZw_dDKnDHCHjDIai_67lqlaSatFBPVeWQWoS1X1GwNLadSQOdXJq46k3XYm"
in_client_id     = "cFR01f6mWygnXN_3i6ZatQ"
in_client_secret = "ZeHWMXzZFei3YXPOnGRsJenPar0tHw"
in_user_agent    = "r/cat by u/LexCutter"
delay = 0

termcolor_colors= ['grey','red','green','yellow','blue','magenta','cyan','white']
# colors that termcolor can use to paint text
# see https://pypi.org/project/termcolor/
# scroll under Text Properties

cache_size_cap_universal=30
# cache is a list of submission url's, used to identifiy duplicates, and not send them if found
# capped at a sertain size, to prevent extensive increase in memory usage

universal_unwanted_content = ["#porn", "porn", "nsfw"]
# universal_unwanted_content is a list of keywords that may appear in a title of a post we dont want

subreddit_list = {
    #'subname':      ['subname', 'webhookname',  delay, [                             unwanted content                                      ], [ wanted flair for pictures ], [ wanted flair for video ]
    'cats':          ['cats'   ,  catswebhook ,  delay, ["rescue", "what is this", "doctor", "help", "consult", "advice", "gender", "please"], [      "Cat Picture"        ], [        "Video"         ] ],
#    'softwaregore': ['softwaregore', proxywebhook, delay],
#    'hardwaregore': ['hardwaregore', proxywebhook, delay],
    'unixporn':     ['unixporn', proxyunixwebhook, delay, [], ['Screenshot'], []]
}

# Below are explanations on some keys in the subreddit_list dictionary that may be missunderstood 

# Unwanted content are keywords that could appear in the titles of posts that we arent looking for.
# For example, in the cats subreddit there are posts of cute cats which we want,
# and there are posts of people looking for advice on something cat related which we dont want
# but these undesirable posts arent always marked with an advice flair or similar, 
# rather they are marked with the 'Cat picture' flair, which we are looking for,
# which then doesnt get stopped by the system, and in the end we get a picture of cat flee's.
# To prevent this, we look for sertain keywords that 
# people looking for advice (in this example) might use in the title.

# Wanted flair for pictures are flair keywords that we want a post with a picture to have

# Wanted flair for video are flair keywords that we want a post with a video to have

reddit = praw.Reddit(
    client_id=in_client_id,
    client_secret=in_client_secret,
    user_agent=in_user_agent
)

print(">Connected!", "\n>Running Service...")


def reddit_thread(subname, webhook, delay, unwanted_content, wanted_flair_picture, wanted_flair_video):
    cache = list()
    # list of submission url's, used to identifiy duplicates, and not send them if found
    # capped at a sertain size, to prevent extensive increase in memory usage
    cache_size_cap = cache_size_cap_universal

    subnameC = colored(" "+subname+" ", random.choice(termcolor_colors), attrs=['reverse', 'bold'])
    #subnameC is a colored version of the subreddit name ( this is only for looks :D )
    seperatorC = colored("#################################################", 'grey', attrs=['bold'])
    #seperatorC is just text used to make the program's text output more readable (seperates submissions)
    postedC = colored("   >>>posted", 'green', attrs=['reverse', 'bold', 'blink'])
    #postedC is just text that pulses to notify of a successfull post

    print(">Started a service for subreddit: ", subnameC)
    for submission in reddit.subreddit(subname).stream.submissions(skip_existing=True):
        try:
            if submission.url not in cache:
                cache.append(submission.url)
                randhex = hex(random.randint(0, 10000))
                #print("FLAIR TEXT", submission.link_flair_text)
                #print("IS OVER 18? ", submission.over_18, type(submission.over_18))

                print(randhex, subnameC, " >Got a Submission \"", submission.title, '\"')
                print(randhex, subnameC, "   >Checking if its not NSFW")
                if not submission.over_18 and not any(x.lower() in str(submission.title).lower() + str(submission.selftext).lower() for x in universal_unwanted_content + unwanted_content):
                    print(randhex, subnameC, "    >NOT NSFW, doesnt have unwanted content")
                    print(randhex, subnameC, " >Checking if its a picture")
                    if 'i.redd.it' in submission.url and any(x in submission.link_flair_text for x in wanted_flair_picture):
                        print(randhex, subnameC,"   >>its a picture")
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
                        print(randhex, subnameC, postedC)
                        print(randhex, subnameC,"   ", response)
                    else:
                        print(randhex, subnameC, "   >NOT a picture")
                        print(randhex, subnameC, "   Was 'i.redd.it' in submission.url? ", 'i.redd.it' in submission.url)
                        print(randhex, subnameC, "   Was wanted flair in submission.link_flair_text? ", any(x in submission.link_flair_text for x in wanted_flair_picture))

                        print(randhex, subnameC, " >Checking if its a video")
                        if submission.is_video and any(x in submission.link_flair_text for x in wanted_flair_video):
                            print(randhex, subnameC,"   >>its a video")
                            url_object = r.head(submission.url, allow_redirects=True)
                            payload = {
                                "content": str(url_object.url)
                            }
                            response = r.post(webhook, json = payload)
                            print(randhex, subnameC, postedC)
                            print(randhex, response)
                        else:
                            print(randhex, subnameC, "   >NOT a video")
                            print(randhex, subnameC, "   Did submission.is_video evaluate to True? ", submission.is_video)
                            print(randhex, subnameC, "   Was wanted flair in submission.link_flair_text? ", any(x in submission.link_flair_text for x in wanted_flair_video))
                    print(randhex, subnameC, " >DONE")
                else:
                    if submission.over_18: 
                        print(randhex, subnameC, "   >Submission marked as OVER 18")
                    if any(x in submission.title for x in universal_unwanted_content + unwanted_content + list((y.upper() for y in unwanted_content)) + list((z.lower() for z in unwanted_content))):
                        print(randhex, subnameC, "   >Unwanted content was in submission title")
                
                if len(cache)>cache_size_cap:
                    cache.pop(0)
                print("CACHE SIZE: ", len(cache))
                print(seperatorC)
                sleep(delay)
            else:
                print(randhex, subnameC, " >DUPLICATE")
        except Exception as e:
            print('Error in ', subnameC, ': ', e)
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
            subreddit_list[subreddit][2],
            subreddit_list[subreddit][3],
            subreddit_list[subreddit][4],
            subreddit_list[subreddit][5],
        ]
        thread_list.append(
            threading.Thread(target=reddit_thread, args = arguments, daemon=True)
        )
        thread_list[index].start()
    main()
