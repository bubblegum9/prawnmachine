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
    import praw
    import requests as r
    import os
    from time import sleep
    import threading
    import random
except Exception as e:
    print(e, "\n")
    sys.exit("Error while trying to import required libraries (did you install the dependencies?)")

random.seed()

print(">Starting...")

catswebhook      = "https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay"
proxywebhook     = "https://discord.com/api/webhooks/892342475681853460/eq6jJOvtUxu4JBE3AWg4nkBo0rWTpWDPWSuM-j7tZtYix1PqhxNEE4WgP6s9SQrELoGH"
proxyunixwebhook = "https://discord.com/api/webhooks/993542686122459186/n4xl7dSajgH9YOtO6VmOQy5HSLtCktDSnSGMLrJHzyDejX1M925FAcFiFe5PwgQ5F1ax"
in_client_id     = "cFR01f6mWygnXN_3i6ZatQ"
in_client_secret = "ZeHWMXzZFei3YXPOnGRsJenPar0tHw"
in_user_agent    = "r/cat by u/LexCutter"
delay = 0

universal_unwanted_content = ["#porn", "porn", "nsfw", "NSFW"]
# universal_unwanted_content is a list of keywords that may appear in a title of a post we dont want

subreddit_list = {
    #'subname':      ['subname', 'webhookname', 'delay', [                             unwanted content                                  ], [ wanted flair for pictures ], [ wanted flair for video ]
    'cats':          ['cats'   ,  catswebhook ,  delay , ["rescue", "What is this", "what is this", "doctor", "help", "consult", "advice"], [      "Cat Picture"        ], [        "Video"         ] ]
#    'softwaregore': ['softwaregore', proxywebhook, delay],
#    'hardwaregore': ['hardwaregore', proxywebhook, delay],
#    'unixporn':     ['unixporn', proxyunixwebhook, delay]
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


def reddit_thread(subreddit_name, webhook, delay, unwanted_content, wanted_flair_picture, wanted_flair_video):
    print(">Started a service for subreddit: ", subreddit_name)
    try:
        for submission in reddit.subreddit(subreddit_name).stream.submissions(skip_existing=True):
            randhex = hex(random.randint(0, 10000))
            #print("FLAIR TEXT", submission.link_flair_text)
            #print("IS OVER 18? ", submission.over_18, type(submission.over_18))

            print(randhex, subreddit_name, " >Got a Submission \"", submission.title, '\"')
            print(randhex, subreddit_name, "   >Checking if its not NSFW")
            if not submission.over_18 and not any(x in submission.title for x in universal_unwanted_content + unwanted_content):
                print(randhex, subreddit_name, "   >NOT NSFW")
                print(randhex, subreddit_name, " >Checking if its a picture")
                if 'i.redd.it' in submission.url and any(x in submission.link_flair_text for x in wanted_flair_picture):
                    print(randhex, subreddit_name,"   >>its a picture")
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
                    print(randhex, subreddit_name,"   >>>posted")
                    print(randhex, subreddit_name,"   ", response)
                else:
                    print(randhex, subreddit_name, "   >NOT a picture")
                    print(randhex, subreddit_name, "   Was 'i.redd.it' in submission.url? ", 'i.redd.it' in submission.url)
                    print(randhex, subreddit_name, "   Was wanted flair in submission.link_flair_text? ", any(x in submission.link_flair_text for x in wanted_flair_picture))

                    print(randhex, subreddit_name, " >Checking if its a video")
                    if submission.is_video and any(x in submission.link_flair_text for x in wanted_flair_video):
                        print(randhex, subreddit_name,"   >>its a video")
                        url_object = r.head(submission.url, allow_redirects=True)
                        payload = {
                            "content": str(url_object.url)
                        }
                        response = r.post(webhook, json = payload)
                        print(randhex, subreddit_name,"   >>>posted")
                        print(randhex, response)
                    else:
                        print(randhex, subreddit_name, "   >NOT a video")
                        print(randhex, subreddit_name, "   Did submission.is_video evaluate to True? ", submission.is_video)
                        print(randhex, subreddit_name, "   Was wanted flair in submission.link_flair_text? ", any(x in submission.link_flair_text for x in wanted_flair_video))

                print(randhex, subreddit_name, " >DONE\n")
                
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
