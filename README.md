# Searching in stealer logs files for passwords and logins

This is a version of Python script for searching phrases in Stealer logs files e.g. Vidar, Racoon.

# Config
To run the script execute `python stealer_search.py`

Required tools/packages are in `requirements.txt` and `requirements_linux.txt`

# How it works?
1. Unpack zip/rar/7z into directory with use of provided passwords (if archive is not protected with password it will still be unpacked). Every archive has respective dir with it name. Also, detect and unpack archives in parts.
2. rg for phrases in unpacked location - rg is done only for `*.txt` files.
3. raw results are saved in `WYNIKI.txt` file
4. based on raw `WYNIKI.txt` the html file for better user experience is created - `WYNIKI.html`
5. results are also divided into 3 html files: Passwords, Cookies, Other

## For better performance -mnt switch is added in 7z commands - please addapt it to your system!

# Info
The whole script has been redesigned and now its a Python script instead of bash - old version is in `bash_version_old`
