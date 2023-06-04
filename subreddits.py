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

universal_unwanted_content = ["#porn", "porn", "nsfw"]
# universal_unwanted_content is a list of keywords that may appear in a title of a post we dont want
# make list empty it that is your preferance

subreddit_list = {
    #'subname':[
    #   'subname',
    #   'webhook',
    #   delay,
    #   [unwanted content],
    #   [wanted flair for pictures],
    #   [wanted flair for video]
    #]
    'cats':[
        'cats',
        'https://discord.com/api/webhooks/960696215199170642/ajKxVGXVfeTW7f9AfYYcdtSBn5K0xrXqluTHvQaQiMn9s8cv7bpyKRXct751sHte48Ay',
        0,
        ["#porn", "porn", "nsfw"],
        ['Cat Picture', 'Humor'],
        ['Workflow']
    ],
    'unixporn':[
        'unixporn',
        'https://discord.com/api/webhooks/1111023590322749540/F7VDon72VY3shNnRe1GsM1LkAD2w289cvXGYHlT3uiwoqjjGPVWHlTHuzz1gpqTUzY45',
        0,
        ['#porn', "nsfw"],
        ['Screenshot', 'Material', 'Workflow'],
        []
    ]
}

