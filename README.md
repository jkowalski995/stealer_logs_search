# Searching in stealer logs files for passwords and logins

This is an initial version of Bash script for searching phrases in Stealer logs files e.g. Vidar, Racoon.

# Config
To run application edit `config.yaml` and provide required paths (3).

`scrypt.sh` must have -rwxrwxrwx permissions so before run execute `chmod +<missing_permissions> scrypt.sh`

To run the script execute `./scrypt.sh`

Required tools/packages are in `requirements.txt`

# How it works?
1. Unpack zip/rar/7z into directory with use of provided passwords (if archive is not protected with password it will still be unpacked). Every archive has respective dir with it name
2. Scan for files extensions (exclude *.txt, *.TXT, *.jpg) and move unneccesary extensions into tmp dir
3. rg for phrases in unpacked location and save results into provided directory to results.txt

# Info
I know that this script is not perfect and has some bugs (e.g. attempting to extract more than once), but for now it is working perfectly for me.
