#!/bin/sh

echo $1
#a = reg-dhc-int.app.corpintra.net/dailysanity123/centos:latest
#echo $a
docker push $1
#docker push reg-dhc-int.app.corpintra.net/dailysanity123/centos:latest 
