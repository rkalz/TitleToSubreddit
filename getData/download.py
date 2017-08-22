import praw
import os
from multiprocessing.dummy import Pool as ThreadPool
from getData import searchReddit

import datetime
import time

from credentials import *
MONTH_IN_SECONDS = 2629746
dir = os.getcwd() + "\\data\\"

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
    dts = datetime.datetime.utcnow()
    lastTime = int(time.mktime(dts.timetuple()) + dts.microsecond/1e6)
    monthAgo = int(lastTime - MONTH_IN_SECONDS)
    f = open(dir + name + ".txt", "w+")
    failCount = 0

    while parsed < 70000:
        print(name + ": Getting posts")
        query = "(subreddit:" + name.lower() + " AND created_utc:>" + str(monthAgo) + " AND created_utc:<" + str(lastTime) + " AND score:>99)&size=1000"
        submissions = searchReddit.reddit_elasticsearch_title(query)
        if len(submissions) != 0:
            failCount = 0
            print(name + ": Received " + str(len(submissions)) + " posts!")
            for title in submissions:
                if parsed < 70000:
                    f.write(remove_special_characters(title) + '\n')
                    parsed += 1
                else:
                    break
            print(name + ": " + str(parsed) + " posts added. " + str(70000 - parsed) + " to go.")
        else:
            print(name +": No posts received! Retrying... (" + str(failCount) + ")")
            if failCount == 10:
                print(name + ": ERROR! No submissions received!")
                break
            failCount += 1

        lastTime = int(monthAgo - 1)
        monthAgo = int(lastTime - MONTH_IN_SECONDS)

    print(name + ": Complete!")
    f.close()

print("signing into reddit")
reddit = praw.Reddit(username=username,password=password, client_id=client_id,
                     client_secret=client_secret,user_agent=user_agent)
print("signed into reddit")

print("getting list of subreddits")
subreddits = list(reddit.user.subreddits(limit=8))
print("got list of subreddits")

pool = ThreadPool(8)

pool.map(get_top_submissions,subreddits)

pool.close()
pool.join()

print("done")
