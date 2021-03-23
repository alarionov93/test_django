#!/bin/bash

base_v=v0.0.
# commit amd push to git
git add *
echo -n "Enter commit msg and press [ENTER]: "
read msg
git commit -a -m "$msg"
echo "..and fix some \xf0\x9f\x92\xa9"
git push
ver_num=$(cat version.txt | tail -1)
git tag "$base_v"$((ver_num+1))
git push --tags
echo $((ver_num+1))\r\n >> version.txt
echo '\xf0\x9f\xa4\x98'
echo '\xf0\x9f\x8d\xba'