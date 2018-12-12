#!/bin/sh

echo $1
#a = registry_url/dailysanity123/centos:latest
#echo $a
docker push $1
#docker push registry_url/dailysanity123/centos:latest 
