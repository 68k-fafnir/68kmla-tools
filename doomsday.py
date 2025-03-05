import requests
import sys

import concurrent.futures

FORUM_URL = '68kmla.org'
START_POST = 1
BIG_NUMBER = 100000  # this should be larger than the total number of posts

MAX_WORKERS = 1000 # max number of concurent threads

# NEVER SHARE ANY OF THESE IT WILL GIVE AWAY YOUR ACCOUNT
if len(sys.argv) == 4:
    xf_session = sys.argv[1]
    xf_csrf = sys.argv[2]
    xf_user = sys.argv[3]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Referer': 'https://68kmla.org/bb/index.php', 'DNT': '1', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Connection': 'keep-alive', 'Cookie': 'SERVERID=vWeb1; xf_session='+xf_session+'; xf_csrf='+xf_csrf+'; xf_user='+xf_user}
else:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Referer': 'https://68kmla.org/bb/index.php', 'DNT': '1', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Connection': 'keep-alive'}
    
fail_404s = 0
read_fails = 0
read_goods = 0
errors_in_a_row = 0

base_path = "https://" + FORUM_URL + "/bb/index.php?threads/foo."

def save_thread(threadid):
    global fail_404s
    global read_fails
    global read_goods
    global errors_in_a_row

    thread_url = base_path + str(threadid)

    r = requests.get(thread_url, headers=headers)
    # the actual thread title. use this to determine when we've read every page. also, don't parse html like this
    human_title = r.text.split('<h1 class="p-title-value">')[-1].split('</h1>')[0]
    # tab title can show 404 message
    tab_title = r.text.split('<title>')[1].split('</title>')[0]

    f = open("threads/"+str(threadid)+".html", "x")
    f.write(r.text)
    f.close

    if '404' in tab_title:
        fail_404s += 1
        errors_in_a_row += 1
        print("404: " + str(threadid))
        if errors_in_a_row >= 10:
            return("10 failed reads in a row. Either we've read every thread, the site is down, or I broke the code (hint: it's probably 3)\n\n"+str(read_goods+read_fails+fail_404s)+" total threads\n"+str(read_goods)+" sucessful reads\n"+str(read_fails)+" failed reads\n"+str(fail_404s)+" 404s")
    elif human_title.lower() == "oops! we ran into some problems. | 68kmla":
        read_fails += 1
        errors_in_a_row += 1
        print("fail to read: " + str(threadid))
        if errors_in_a_row >= 10:
            return("10 failed reads in a row. Either we've read every thread, the site is down, or I broke the code (hint: it's probably 3)\n\n"+str(read_goods+read_fails+fail_404s)+" total threads\n"+str(read_goods)+" sucessful reads\n" + str(read_fails)+" failed reads\n"+str(fail_404s)+" 404s")
    elif 'log in' in tab_title.lower():
        read_fails += 1
        errors_in_a_row = 0
        print ("login: "+str(threadid))
    else:
        read_goods += 1
        errors_in_a_row = 0
        print("good: " + str(threadid))

def doomsday_loop(start_post_id, latest_post_id):
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

    for threadid in range(start_post_id, latest_post_id+1):
        pool.submit(save_thread(threadid))

    pool.shutdown(wait=True)

    return("done!\n\n"+str(read_goods+read_fails-errors_in_a_row)+" total threads\n" + str(read_goods)+" sucessful reads\n" + str(read_fails)+" failed reads")

print(doomsday_loop(START_POST, BIG_NUMBER))