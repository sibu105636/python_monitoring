#!/bin/bash

a=`ps -ef|grep -i python|grep -i script_scheduler.py`
#echo $a
if [ ! -z "$a" ]
then
	echo "python exporter is running"
else
	echo "python exporter is down!!!,starting the exporter"
	`nohup python /home/sitripa/quay_sanity/script_scheduler.py  2>>/home/sitripa/quay_sanity/error.log 1>/home/sitripa/quay_sanity/output.log &`
fi 
