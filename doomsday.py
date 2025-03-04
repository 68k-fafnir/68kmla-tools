import requests

FORUM_URL = '68kmla.org'
START_POST = 1
BIG_NUMBER = 100000  #this should be larger than the total number of posts

def doomsday_prep(url, start_post_id, latest_post_id):
    fail_404s = 0
    read_fails = 0
    read_goods = 0
    errors_in_a_row = 0

    base_path = "https://" + url + "/bb/index.php/threads?foo."
    for threadid in range(start_post_id, latest_post_id+1):
        thread_url = base_path + str(threadid)

        r = requests.get(thread_url) # TODO: auth
        # the actual thread title. use this to determine when we've read every page. also, don't parse html like this
        human_title = r.text.split('<h1 class="p-title-value">')[-1].split('</h1>')[0]
        # tab title can show 404 message
        tab_title = r.text.split('<title>')[1].split('</title>')[0]

        if '404' in tab_title:
            fail_404s += 1
            errors_in_a_row += 1
            print("404: " + str(threadid))
            if errors_in_a_row >= 10:
                return("10 failed reads in a row. Either we've read every thread, the site is down, or I broke the code (hint: it's probably 3)\n\n"+str(read_goods+read_fails+fail_404s)+" total threads\n"+str(read_goods)+" sucessful reads\n"+str(read_fails)+" failed reads\n"+str(fail_404s)+" 404s")
        elif human_title.lower == "oops! we ran into some problems. | 68kmla":
            read_fails += 1
            errors_in_a_row += 1
            print("fail to read: " + str(threadid))
            if errors_in_a_row >= 10:
                return("10 failed reads in a row. Either we've read every thread, the site is down, or I broke the code (hint: it's probably 3)\n\n"+str(read_goods+read_fails+fail_404s)+" total threads\n"+str(read_goods)+" sucessful reads\n" + str(read_fails)+" failed reads\n"+str(fail_404s)+" 404s")
        else:
            read_goods += 1
            errors_in_a_row = 0
            print("good: " + str(threadid))
    return("done!\n\n"+str(read_goods+read_fails-errors_in_a_row)+" total threads\n" + str(read_goods)+" sucessful reads\n" + str(read_fails)+" failed reads")

print(doomsday_prep(FORUM_URL, START_POST, BIG_NUMBER))