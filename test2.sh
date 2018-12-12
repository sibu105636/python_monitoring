#!/bin/sh
a=`docker images|grep redis|awk '{print $3}'`
echo $a
if [ ! -z "$a" ]
then
   echo "image already available locally,deleting the local image"
   docker rmi -f $a
else
   echo "image not available locally, pulling it from registry"
fi
docker pull reg-dhc.app.corpintra.net/dailysanity123/redis:latest 
