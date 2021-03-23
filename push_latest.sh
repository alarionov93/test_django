#!/bin/bash

base_v=v0.0.
# commit amd push to git
git add *
echo -n "Enter commit msg and press [ENTER]: "
read msg
git commit -a -m "$msg"
git push
ver_num=$(cat version.txt | tail -1)
echo git tag "$base_v"$((ver_num))
echo $((ver_num)) >> version.txt

