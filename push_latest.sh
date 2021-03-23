#!/bin/bash

base_v=v0.0.
# commit amd push to git
git add *
echo -n "Enter commit msg and press [ENTER]: "
read msg
git commit -a -m "$msg ..and fix some \U0001f4a9"
echo "..and fix some \U0001f4a9"
git push
ver_num=$(cat version.txt | tail -1)
git tag "$base_v"$((ver_num+1))
echo $((ver_num+1))\r\n >> version.txt
echo '\U0001f918'
echo '\U0001f37a'