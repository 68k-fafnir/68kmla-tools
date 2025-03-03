from pathlib import Path
import csv
import requests

db_path = Path('titles.csv')

FORUM_URL = '68kmla.org'
LATEST_POST = 49471

def save_titles(url, latest_post_id):
    if db_path.is_file():
        return "Error: db file already exists. please delete it, and run again"

    base_path = "https://" + url + "/bb/index.php?threads/foo."

    # don't do this
    db = open(db_path, "x")
    db.close()

    db = open(db_path, "w", newline='')
    dbwriter = csv.writer(db, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for threadid in range(1, latest_post_id+1):
        thread_url = base_path + int(threadid)
        r = requests.get(thread_url) # TODO: auth
        # the actual thread title. also, don't parse html like this
        human_title = r.text.split('<h1 class="p-title-value">')[1].split('</h1>')[0]
        if human_title == "Oops! We ran into some problems. | 68kMLA":
            print("fail to read: " + str(threadid))
            dbwriter.writerow([str(threadid), 'ERROR', 'ERROR', 'ERROR'])
        else:
            # the title that's in the url
            url_title = r.text.split('content="https://68kmla.org/bb/index.php?threads/')[1].split('.')[0]
            # the title of the tab
            web_title = r.text.split('<title>')[1].split('</title>')[0]

            print("sucess read: " + str(threadid))
            dbwriter.writerow([str(threadid), url_title, human_title, web_title])

        

print(save_titles(FORUM_URL, LATEST_POST))