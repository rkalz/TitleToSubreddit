import praw
import os
from multiprocessing.dummy import Pool as ThreadPool

from credentials import *

def remove_special_characters(string):
    out = ''
    string.encode("utf8").decode("utf8")
    string = string.lower()

    for c in string:
        if c is ' ':
            out += c
        num = ord(c)
        if num >= 97 and num <= 122:
            out += c

    out = ' '.join(out.split())
    return out

def get_top_submissions(subreddit):
    name = subreddit.display_name
    parsed = 0

    print("getting top submissions from /r/" + name)
    f = open(dir + name + ".txt", "w+")
    print(name + ": fetching submissions 0 to 99")
    posts = list(reddit.get("/r/"+name+"/top",params={"limit" : 100}))
    parsed += 100

    while parsed <= 1000:
        print(name + ": writing to " + name + ".txt")
        for submission in posts:
            title = remove_special_characters(submission.title)
            f.write(title + "\n")
        if len(posts) == 0:
            break
        lastId = posts[-1].fullname
        print(name + ": fetching submissions " + str(parsed) + " to " + str(parsed+99))
        posts = list(reddit.get("/r/"+name+"/top",params={"limit" : 100, "after" : lastId}))
        parsed += 100

    f.close()

dir = os.getcwd() + "\\data\\"

print("signing into reddit")
reddit = praw.Reddit(username=username,password=password, client_id=client_id,
                     client_secret=client_secret,user_agent=user_agent)
print("signed into reddit")

print("getting list of subreddits")
subreddits = list(reddit.user.subreddits(limit=15))
print("got list of subreddits")
f = open(dir + "categories.py" ,"w+")
f.write("categories = [")
for sub in subreddits:
    f.write("\"" + sub.display_name + "\"" + ",")
f.write("]")
f.close()

pool = ThreadPool(15)

pool.map(get_top_submissions,subreddits)

pool.close()
pool.join()

print("done")
