#!/bin/bash
HOSTNAME="$1"

cat file_list.txt | parallel -j <number_of_jobs> rsync -avz {} bxqml233@${HOSTNAME}:/home/bxqml233
