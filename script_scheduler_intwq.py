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
#schedule.every(5).minutes.do(quayValidation) 
#schedule.every(5).minutes

class JsonCollector(object):
  def __init__(self, endpoint):
    self._endpoint = endpoint
  
  def collect(self):
    import pdb;pdb.set_trace()
    release_validation_metric_emea = CounterMetricFamily('quay_validation_emea', 'To get the validation status of quay release', labels=['release_validation_status_emea'])
    for quayOperation in quay_emea_cache.iterkeys():
      release_validation_metric_emea.add_metric([quayOperation],
          quay_emea_cache[quayOperation])
    yield release_validation_metric_emea

    import pdb;pdb.set_trace()
    release_validation_metric_apac = CounterMetricFamily('quay_validation_apac', 'To get the validation status of quay release', labels=['release_validation_status_apac'])
    for quayOperation in quay_apac_cache.iterkeys():
      release_validation_metric_apac.add_metric([quayOperation],
          quay_apac_cache[quayOperation])
    yield release_validation_metric_apac


  

    push_speed_metric_emea = CounterMetricFamily('push_speed_emea', 'To get the push speed', labels=['push_speed_emea'])
    if 'image_push_Speed' in quayPushSpeed_emea_cache :
      push_speed_metric_emea.add_metric(['image_push_Speed'],
           quayPushSpeed_emea_cache['image_push_Speed'])
    yield push_speed_metric_emea 

    push_speed_metric_apac = CounterMetricFamily('push_speed_apac', 'To get the push speed', labels=['push_speed_apac'])
    if 'image_push_Speed' in quayPushSpeed_apac_cache :
      push_speed_metric_apac.add_metric(['image_push_Speed'],
           quayPushSpeed_apac_cache['image_push_Speed'])
    yield push_speed_metric_apac




    pull_speed_metric_emea = CounterMetricFamily('pull_speed_emea', 'To get the pull speed', labels=['pull_speed_emea'])
    if 'image_pull_Speed' in quayPullSpeed_emea_cache :
      pull_speed_metric_emea.add_metric(['image_pull_Speed'],
           quayPullSpeed_emea_cache['image_pull_Speed'])
    yield pull_speed_metric_emea

    pull_speed_metric_apac = CounterMetricFamily('pull_speed_apac', 'To get the pull speed', labels=['pull_speed_apac'])
    if 'image_pull_Speed' in quayPullSpeed_apac_cache :
      pull_speed_metric_apac.add_metric(['image_pull_Speed'],
           quayPullSpeed_apac_cache['image_pull_Speed'])
    yield pull_speed_metric_apac

 
    
    
 


if __name__ == '__main__':
  # Usage: json_exporter.py port endpoint
  start_http_server(9193)
  REGISTRY.register(JsonCollector('https://git-dhc-int.app.corpintra.net/rest/api/1.0/admin/groups'))

  while True:

#	repolist = ('centos', 'redis')
#	i = 0
#	for i in repolist:
		test1 = quay_test('image_name', 'registry_yrl', 'token', 359, 'EMEA')
    		test1.quayValidation()
		test2 = quay_test('image_name', 'registry_yrl', 'token', 107, 'APAC')
		test2.quayValidation()
