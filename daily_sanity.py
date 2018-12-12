#!/usr/bin/python
from shutil import copyfile
from subprocess import Popen, PIPE
from threading import Thread
#from Queue import Queue
import os
import argparse
import json
import requests
import subprocess
import sys
from diskcache import Cache
import time

quay_emea_cache = Cache('/tmp/quayResult_emea')
quayPushSpeed_emea_cache = Cache('/tmp/quayPushSpeed_emea')
quayPullSpeed_emea_cache = Cache('/tmp/quayPullSpeed_emea')
quay_apac_cache = Cache('/tmp/quayResult_apac')
quayPushSpeed_apac_cache = Cache('/tmp/quayPushSpeed_apac')
quayPullSpeed_apac_cache = Cache('/tmp/quayPullSpeed_apac')

class quay_test:
	def __init__(self, name, url, token, size, region):
		self.repo_address = url
		self.repo_ref = "/dailysanity123"
		self.repo_url = self.repo_address + self.repo_ref
		self.container_name = name
		self.container_tag = "latest"
		self.token = token
		self.image_size = size
		self.region = region
		self.image_url = self.repo_address + self.repo_ref + '/' + self.container_name
		self.full_repo_add = self.repo_address + self.repo_ref + '/' + self.container_name + ':' + self.container_tag
#api_endpt = "https://reg-dhc-int.app.corpintra.net/api/v1/repository/dailysanity123"


	def reg_login(self):
    		print ("logging in to quay registry")
   	 	copyfile('/home/sitripa/quay_sanity_int/config/config.json', '/root/.docker/config.json')


	def push_container(self):
		print self.full_repo_add
    		print ("checking if the image is available locally")
    		subprocess.call(['./test3.sh', self.image_url])
    		print ("pushing image to repo")
    		start_time = time.time()
#    build_command = subprocess.call(['docker push reg-dhc-int.app.corpintra.net/dailysanity123/postgres:latest > /dev/null 2>&2', shell=true])
    		build_command = subprocess.call(['./test1.sh', self.full_repo_add])
    		if build_command == 0:
      			end_time = time.time()
      			action_time = end_time - start_time
      			push_speed = self.image_size / action_time
			if self.region == 'EMEA':
				quay_emea_cache['push_container']=1
      				quayPushSpeed_emea_cache['image_push_Speed']=push_speed 
      				print ("image push speed emea is", push_speed, "mb per/sec")
			else:
				quay_apac_cache['push_container']=1
                                quayPushSpeed_apac_cache['image_push_Speed']=push_speed
                                print ("image push speed apac is", push_speed, "mb per/sec")
    		else:
			if self.region == 'EMEA':
      				quay_emea_cache['push_container']=0 
      				print ("Error while pushing emea")
			else:
				quay_apac_cache['push_container']=0
                                print ("Error while pushing apac")

	def delete_local_images(self):
    		start_time = time.time()
    		delete_local_images_command = Popen(['docker', 'rmi', '-' + 'f', self.full_repo_add])
    		delete_local_images_command.wait()
    		end_time = time.time()
    		action_time = end_time - start_time
    		print ("local image has been deleted in", action_time)

	def pull_container(self):
    		print ("pulling image from registry")
    		start_time = time.time()
    		build_command = subprocess.call(['./test2.sh', self.full_repo_add])
    		if build_command == 0:
       			end_time = time.time()
       			action_time = end_time - start_time
       			pull_speed = self.image_size / action_time
			if self.region == 'EMEA':
				quay_emea_cache['pull_container']=1
       				quayPullSpeed_emea_cache['image_pull_Speed']=pull_speed
       				print ("image pull speed emea is", pull_speed, "mb per/sec")
			else:
				quay_apac_cache['pull_container']=1
                                quayPullSpeed_apac_cache['image_pull_Speed']=pull_speed
                                print ("image pull speed apac is", pull_speed, "mb per/sec")
    		else:
			if self.region == 'EMEA':
       				quay_emea_cache['pull_container']=0 
       				print ("Error while pulling emea")
			else:
				quay_apac_cache['push_container']=0
                                print ("Error while pushing apac")



	def delete_reg_image(self):
    		url='https://' + self.repo_address + '/api/v1/repository/dailysanity123%2F' + self.container_name
    		headers = {"Authorization": "Bearer " + self.token, "Content-Type": "application/json"}
    		r = requests.get(url, verify=False,  headers=headers)
       		m = requests.delete(url, verify=False,  headers=headers)
       		if m.status_code == 204:
			if self.region == 'EMEA':
				quay_apac_cache['del_image']=1
                                print ("image deleted from emea")
			else:
				quay_apac_cache['del_image']=1
                                print ("image deleted from apac") 	      
         		print(r.status_code)
         		print(r.text)
         		print ("Repo has been deleted from quay registry")
       		else:
			if self.region == 'EMEA':
         			quay_emea_cache['del_image']=0
                                print ("error deleteing emea image")
			else:
                                quay_apac_cache['del_image']=0
                                print ("error deleteing apac image")
         		#print ("error while deleting repo")
       			#print ("repo does not exists")


	def docker_logout(self):
    		logout_command = Popen(['docker', 'logout', self.repo_url])





	def quayValidation(self):
  		self.reg_login()
  		self.push_container()
  		self.delete_local_images()
  		self.pull_container()
  		self.delete_reg_image()
  		self.docker_logout() 
  		time.sleep(30)
