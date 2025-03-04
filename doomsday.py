import requests

FORUM_URL = '68kmla.org'
BIG_NUMBER = 100000  #this should be larger than the total number of posts
START_POST = 1

def doomsday_prep(url, start_post_id, latest_post_id):
    for threadid in range(start_post_id, latest_post_id+1):
        continue
    return("done")

print(doomsday_prep(FORUM_URL, START_POST, BIG_NUMBER))