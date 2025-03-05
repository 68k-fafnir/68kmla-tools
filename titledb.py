from pathlib import Path
import csv
import requests
import sys

db_path = Path('titles.csv')

FORUM_URL = '68kmla.org'
BIG_NUMBER = 100000  #this should be larger than the total number of posts
START_POST = 1

if len(sys.argv) == 4:
    xf_session = sys.argv[1]
    xf_csrf = sys.argv[2]
    xf_user = sys.argv[3]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br, zstd',
               'Referer': 'https://68kmla.org/bb/index.php',
               'DNT': '1',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-User': '?1',
               'Connection': 'keep-alive',
               'Cookie': 'SERVERID=vWeb1; xf_session='+xf_session+'; xf_csrf='+xf_csrf+'; xf_user='+xf_user
               }
else:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language': 'en-US,en;q=0.5',
               'Accept-Encoding': 'gzip, deflate, br, zstd',
               'Referer': 'https://68kmla.org/bb/index.php',
               'DNT': '1',
               'Sec-Fetch-Site': 'same-origin',
               'Sec-Fetch-User': '?1',
               'Connection': 'keep-alive',
               }

def save_titles(url, start_post_id, latest_post_id):
    read_sucesses = 0
    read_fails = 0
    read_logins = 0

    errors_in_a_row = 0
    if db_path.is_file():
        return "Error: db file already exists. please delete it, and run again"

    base_path = "https://" + url + "/bb/index.php?threads/foo."

    # don't do this
    db = open(db_path, "x")
    db.close()

    for threadid in range(start_post_id, latest_post_id+1):
        thread_url = base_path + str(threadid)

        r = requests.get(thread_url, headers=headers)
        # the actual thread title. also, don't parse html like this
        human_title = r.text.split('<h1 class="p-title-value">')[1].split('</h1>')[0]

        if human_title == "Oops! We ran into some problems. | 68kMLA":
            human_title = 'ERROR'
            url_title = 'ERROR'
            web_title = 'ERROR'
            read_fails += 1
            errors_in_a_row += 1
            print("fail to read: " + str(threadid))
            if errors_in_a_row >= 10:
                return("10 failed reads in a row. Either we've read every thread, or the site is down.\n\n"+str(read_sucesses+read_logins+read_fails-errors_in_a_row)+" total threads\n" + str(read_sucesses)+" sucessful reads\n" + str(read_logins) + " threads that require login\n" + str(read_fails)+" failed reads")

        elif 'log in' in human_title.lower():
            human_title = 'LOGIN'
            url_title = 'LOGIN'
            web_title = 'LOGIN'
            read_logins += 1
            errors_in_a_row = 0
            print("login protected: " + str(threadid))
        else:
            # the title that's in the url
            url_title = r.text.split('content="https://68kmla.org/bb/index.php?threads/')[1].split('.')[0]
            # the title of the tab
            web_title = r.text.split('<title>')[1].split('</title>')[0]
            read_sucesses += 1
            errors_in_a_row = 0
            print("sucess read: " + str(threadid))
        
        with open(db_path, 'a', newline='') as dbfile:
            writer = csv.writer(dbfile)
            writer.writerow([str(threadid), url_title, human_title, web_title])

    return "done!\n\n"+str(read_sucesses+read_logins+read_fails-errors_in_a_row)+" total threads\n" + str(read_sucesses)+" sucessful reads\n" + str(read_logins) + " threads that require login\n" + str(read_fails)+" failed reads"


print(save_titles(FORUM_URL, START_POST, BIG_NUMBER))