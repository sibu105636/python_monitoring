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


quay_cache = Cache('/tmp/quayResult')
quayPushSpeed_cache = Cache('/tmp/quayPushSpeed')
quayPullSpeed_cache = Cache('/tmp/quayPullSpeed')

iterations = 1
concurrency = 1
repo_address = "reg-dhc.app.corpintra.net"
repo_ref = "/dailysanity123"
repo_url = repo_address + repo_ref
container_name = "redis"
container_tag = "latest"
token = "wcRZhtvgLFAbly3OyCIYioZRRq9lbJIbQcqCQPMt"
#api_endpt = "https://reg-dhc-int.app.corpintra.net/api/v1/repository/dailysanity123"

#work_dir = "memcached"
#build_results_file = "build_results.csv"
push_results_file = "push_results.txt"
#pull_results_file = "pull_results.csv"
#delete_local_results_file = "delete_local_results.csv"

#results_files = [build_results_file, push_results_file, pull_results_file, delete_local_results_file]
#for results_file in results_files:
#    outfile = open(results_file, 'w')
#    outfile.write("iteration,spent_time")
#    outfile.close()

#work_queue = Queue()


def build_container():
#    start_time = time()
    build_command = Popen(['docker', 'build', '--no-cache=true', '-t', repo_url + '/' + container_name + ':' + container_tag, '--file=' + work_dir + '/Dockerfile', work_dir])
#    build_command.wait()
#    end_time = time()
#    action_time = end_time - start_time
    print ("build has been done in", action_time)
#    outfile = open(build_results_file, 'a')
#    outfile.write('\n' + str(iteration) + "," + str(action_time))
#    outfile.close()

def reg_login():
    print ("logging in to quay registry")
    copyfile('/home/sitripa/quay_sanity/config/config.json', '/root/.docker/config.json')


def push_container():
    print ("checking if the image is available locally")
    subprocess.call(['./test3.sh'])
    print ("pushing image to repo")
    start_time = time.time()
#    build_command = subprocess.call(['docker push reg-dhc-int.app.corpintra.net/dailysanity123/postgres:latest > /dev/null 2>&2', shell=true])
    build_command = subprocess.call(['./test1.sh'])
    if build_command == 0:
      quay_cache['push_container']=1 
      end_time = time.time()
      action_time = end_time - start_time
      push_speed = 107 / action_time
      quayPushSpeed_cache['image_push_Speed']=push_speed 
      print ("image push speed is", push_speed, "mb per/sec")
    else:
      quay_cache['push_container']=0 
      print ("Error while pushing")
#      print "aborting the operation"
#      os.system("kill -9 %d"%(os.getpid()))
#    outfile = open(push_results_file, 'a')
#    outfile.write('\n' build_command)
#    outfile.close()


def delete_local_images():
    
    start_time = time.time()
    delete_local_images_command = Popen(['docker', 'rmi', '-' + 'f', repo_url + '/' + container_name + ':' + container_tag])
#   delete_local_images_command=subprocess.call(['./test4.sh'])
    delete_local_images_command.wait()
    end_time = time.time()
    action_time = end_time - start_time
    print ("local image has been deleted in", action_time)
#    outfile = open(delete_local_results_file, 'a')
#    outfile.write('\n' + str(iteration) + "," + str(action_time))
#    outfile.close()


def pull_container():
    print ("pulling image from registry")
    start_time = time.time()
#    build_command = Popen(['docker', 'pull', repo_url + '/' + container_name + ':' + container_tag])
    build_command = subprocess.call(['./test2.sh'])
    if build_command == 0:
       quay_cache['pull_container']=1 
       end_time = time.time()
       action_time = end_time - start_time
       pull_speed = 107 / action_time
       quayPullSpeed_cache['image_pull_Speed']=pull_speed
       print ("image pull speed is", pull_speed, "mb per/sec")
    else:
       quay_cache['pull_container']=0 
       print ("Error while pulling")

#    outfile = open(pull_results_file, 'a')
#    outfile.write('\n' + str(iteration) + "," + str(action_time))
#    outfile.close()

def delete_reg_image():

    url='https://reg-dhc.app.corpintra.net/api/v1/repository/dailysanity123%2Fredis'
#    payload = json.load(open("requests.json"))
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json"}

#    payload = {"slug": "testrepo1", "name": "test7", "project": {"key": "demo2"}}
    r = requests.get(url, verify=False,  headers=headers)
    if r.status_code == 200:
       quay_cache['del_image']=1 
       m = requests.delete(url, verify=False,  headers=headers)
       if m.status_code == 204:       
         print(r.status_code)
         print(r.text)
         print ("Repo has been deleted from quay registry")
       else:
         quay_cache['del_image']=0 
         print ("error while deleting repo")
    else:
       print ("repo does not exists")


def docker_logout():
    logout_command = Popen(['docker', 'logout', repo_url])



#def delete_local_images(iteration):
#    start_time = time()
#    delete_local_images_command = Popen(['docker', 'rmi', repo_url + '/' + container_name + '-' + str(iteration)])
#    delete_local_images_command.wait()
#    end_time = time()
#    action_time = end_time - start_time
#    print "Iteration", iteration, "has been done in", action_time
#    outfile = open(delete_local_results_file, 'a')
#    outfile.write('\n' + str(iteration) + "," + str(action_time))
#    outfile.close()



#def repeat():
#    while work_queue.empty() is False:
#       iteration = work_queue.get_nowait()
#       container_action(iteration)
#       work_queue.task_done()


#def fill_queue(iterations):
#    for iteration in range(1, (iterations + 1)):
#        work_queue.put(iteration)


def quayValidation():
  reg_login()
  push_container()
  delete_local_images()
  pull_container()
  delete_reg_image()
  docker_logout() 
  time.sleep(900)
#container_actions = [reg_login, push_container, delete_local_images, pull_container,delete_reg_image, docker_logout]
#for container_action in container_actions:
#    fill_queue(iterations)
#    for thread_num in range(1, (concurrency + 1)):
#        if work_queue.empty() is True:
#            break
#        worker = Thread(target=repeat)
#        worker.start()
#    work_queue.join()
