from prometheus_client.core import GaugeMetricFamily, CounterMetricFamily
from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time
import schedule
import time
from daily_sanity import *

#schedule.every().day.at("09:10").do(BitbucketValidation) 
schedule.every(5).minutes.do(quayValidation) 

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = endpoint
  
  def collect(self):
    release_validation_metric = CounterMetricFamily('quay_validation', 'To get the validation status of quay release', labels=['release_validation_status'])
    for quayOperation in quay_cache.iterkeys():
      release_validation_metric.add_metric([quayOperation],
          quay_cache[quayOperation])
    yield release_validation_metric  

    push_speed_metric = CounterMetricFamily('push_speed', 'To get the push speed', labels=['push_speed'])
    if 'image_push_Speed' in quayPushSpeed_cache :
      push_speed_metric.add_metric(['image_push_Speed'],
           quayPushSpeed_cache['image_push_Speed'])
    yield push_speed_metric 

    pull_speed_metric = CounterMetricFamily('pull_speed', 'To get the pull speed', labels=['pull_speed'])
    if 'image_pull_Speed' in quayPullSpeed_cache :
      pull_speed_metric.add_metric(['image_pull_Speed'],
           quayPullSpeed_cache['image_pull_Speed'])
    yield pull_speed_metric
 
    
    
 


if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  start_http_server(9192)
  REGISTRY.register(JsonCollector('https://url'))

  while True: 
    #time.sleep(1)
    quayValidation()
    #schedule.run_pending()
