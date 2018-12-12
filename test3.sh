#!/bin/sh

a=`docker images|grep dailysanity123/$1|awk '{print $1}'`
b=`echo $1|cut -f3 -d"/"`
if [ ! -z "$a" ]
then
   echo "image available locally"
else
   echo "image not available locally, fetching from tar file"
   docker load < /home/sitripa/quay_sanity_int/$b.tar
fi
