##test

import praw
import user_data

#ismusic
#multpile filters
#treat seperate words
#add search
#filter by content file type
#add filter bu comment content
#add search outside of saved
#handle crossposts
#leave out comments
#gifs
#nsfw
#tags
#add image poster while video loads
#display_saved
#load multiple images
#add comment section

reddit=None
saved=None

def login(username: str,password: str):

    global reddit

    try:

        reddit=praw.Reddit(client_id="S7v3IfgVUGcn2FD1cmmcwQ",
                           client_secret="A-BL-OqZL-_CV8OcMhXCJldj744rCw",
                           user_agent="better_saved",
                           username=username,
                           password=password)

        reddit.user.me()

        return({"failed": False,"message": f"Successfully logged in as u/{username}."})

    except Exception as error:
        return({"failed": True,"message": str(error)})

def load_saved(limit=None):

    global saved

    saved=reddit.user.me().saved(limit=limit)
    saved=[i for i in saved if isinstance(i,praw.models.reddit.submission.Submission)]
    saved=tuple(saved)

def filter_posts(posts: list,filters: dict):

    filtered=[]

    for i,post in enumerate(posts):

        is_valid=False

        for filterkey in filters:

            if is_valid:
                break

            for datakey in filters[filterkey].keys():

                text=f"(filters['{filterkey}']['{datakey}']"
                text+=f" and filters['{filterkey}']['{datakey}'] {filterkey} str(post.{datakey}))"

                if eval(text):
                    is_valid=True
                    break

        if is_valid:
            filtered.append(post)

    return(filtered)

def get_saved(filters):
    return(filter_posts(saved,filters))

if __name__=='__main__':

    login(user_data.username,user_data.password)

    saved=get_saved({"in": {"subreddit": "anime","author": "","title": ""},
                     "==": {"subreddit": "","author": "","title": ""}},
                     limit=50)

    for post in saved:

        print(f"r/{post.subreddit}\nu/{post.author}\n[{post.title}]")
