#!/bin/bash

a=`ps -ef|grep script_scheduler.py`
#echo $a
if [ ! -z "$a" ]
then
	echo "python exporter is running"
else
	echo "python exporter is down!!!,starting the exporter"
	`nohup python /home/sitripa/quay_sanity/script_scheduler.py > /dev/null &`
fi 
