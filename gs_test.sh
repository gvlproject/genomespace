#!/bin/bash

if [ ! -d "./reports" ]; then
    mkdir "./reports"
fi
folder="$(date +"%d-%m-%y")"
if [ ! -d "./reports/$folder" ]; then
    mkdir "./reports/$folder"
fi
filename="$(date +"%H.%M.%S").txt"
python ./source/GSchrome.py 2> "./reports/$folder/$filename"