#!/bin/bash

# Color codes definition
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No color

echo -e "${RED} THis message is only a informational reminder that to work properly script needs xw permissions. So if any error occurs firstly execute chmod +xw scrypt.sh${NC}"

# Load configuration from YAML file
CONFIG_FILE="config.yaml"
DIR1=$(awk '/dir1/ {print $2}' "$CONFIG_FILE")
DIR2=$(awk '/dir2/ {print $2}' "$CONFIG_FILE")
DIR3=$(awk '/dir3/ {print $2}' "$CONFIG_FILE")
PHRASES=$(awk '/phrases:/ {flag=1; next} /- phrase:/ {flag=0} flag {print}' "$CONFIG_FILE")

echo -e "${GREEN}Config loaded${NC}"

# Unpack archive from dir1 to dir2
mkdir -p "$DIR2"
unrar x "$DIR1"/*.rar "$DIR2"  # Unpack .rar archives
unzip "$DIR1"/*.zip -d "$DIR2"  # Unpack .zip archives

echo -e "${GREEN}Unpacking complete to ${YELLOW} $DIR2 ${NC}"

# Create a temporary directory to move unnecessary files
TMP_DIR="$DIR1/tmp"
mkdir -p "$TMP_DIR"

echo -e "${GREEN}Temporary dir created${YELLOW} $TMP_DIR ${NC}"

# Get list of file extensions after unpacking - exclude *.txt as common stealer log file
output=$(find "$DIR2" -type f ! -name "*.txt" -exec sh -c 'echo "${0##*.}"' {} \; | sort | uniq)

# Define the YAML file path
yaml_file="extensions.yaml"

# Create the YAML file and write the output
echo "$output" | awk 'BEGIN { print "unnecessary_extensions:" } { print "- " $0 }' > "$yaml_file"

echo -e "${GREEN}Extensions list saved to ${YELLOW} $yaml_file ${NC}"

# Load extensions from YAML file
EXTENSIONS_FILE="extensions.yaml"

UNNECESSARY_EXTENSIONS=$(awk '/unnecessary_extensions:/ {flag=1; next} /- / {print}' "$EXTENSIONS_FILE")

# Move files with unnecessary extensions to the temporary directory
for extension in $UNNECESSARY_EXTENSIONS; do
    find "$DIR2" -type f -iname "*.$extension" -exec mv {} "$TMP_DIR" \;
done

echo -e "${GREEN}Unnecessary files moved to ${YELLOW} $TMP_DIR ${NC}"

# Search for phrases in dir2 using rg and save results to dir3
mkdir -p "$DIR3"
for phrase in $PHRASES; do
    rg "$phrase" "$DIR2" > "$DIR3/$phrase.txt"
done

echo -e "${GREEN}rg search done. Results saved in ${YELLOW} $DIR3 ${NC}"
echo -e "${RED}Exit${NC}"
