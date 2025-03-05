# 68kmla-tools

to run the scripts with auth use the following syntax:
`python script.py xf_session xf_csrf xf_user`
xf_session, xf_csrf, and xf_user can be found by looking at the network tab in devtools when you load a forum page. NEVER SHARE THESE THEY GIVE ACCESS TO YOUR ACCOUNT

titledb.py: create a database of all the post titles and their corresponding ids. I use it to find where posts are now after the crash. Should work on any xenforo forum idk.

doomsday.py: download all the forum pages without processing them at all.Should work on any xenforo forum idk.