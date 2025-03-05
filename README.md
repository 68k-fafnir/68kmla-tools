# 68kmla-tools

Some simple scripts I made to backup data from [the 68kmla forums](https://68kmla.org). The scripts can be used with or without login creds to the forum. These tools might work on other xenforo forums.

To run the scripts with auth use the following syntax:

`python script.py xf_session xf_csrf xf_user`

xf_session, xf_csrf, and xf_user can be found by looking at the network tab in devtools when you load a forum page. NEVER SHARE THESE THEY GIVE ACCESS TO YOUR ACCOUNT

titledb.py: Create a database of all the post titles and their corresponding ids. I use it to find where posts are now after the crash.

doomsday.py: Download all the forum pages without processing them at all. If you get a `FileExistsError`, delete the files from the threads directory.