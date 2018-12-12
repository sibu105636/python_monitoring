#!/bin/sh

a=`docker images|grep reg-dhc.app.corpintra.net/dailysanity123/redis|awk '{print $1}'`
echo $a
if [ ! -z "$a" ]
then
   echo "image available locally"
else
   echo "image not available locally, fetching from tar file"
   docker load < /home/sitripa/quay_sanity/redis_prod.tar
fi
