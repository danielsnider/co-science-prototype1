#!/usr/bin/env python

import pika
import cPickle
import numpy as np
import glob
import skimage
import time
import requests


from skimage.viewer import ImageViewer
from matplotlib import pyplot as plt


user = 'guest'
password = 'guest'

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

publish_topic = 'images-d'

ex = channel.exchange_declare(exchange=publish_topic,
                         exchange_type='direct')



# channel.exchange_declare(exchange='images_fanout',
#                          exchange_type='fanout')


# channel.exchange_bind(destination='images_fanout',source=publish_topic) # error, e2e not supported for lvc exchange as source. https://github.com/rabbitmq/rabbitmq-lvc-exchange/issues/9

channel.confirm_delivery()

for filename in glob.iglob('./images/*'):
  print('%s' % filename)
  while True:
    queue_details_url = 'http://localhost:15672/api/queues/%2f/' + publish_topic
    r = requests.get(queue_details_url,auth=(user,password))
    queue = r.json()
    q_len = queue['messages']
    # q = channel.queue_declare(publish_topic)
    # q_len = q.method.message_count
    print('queue length: %s' % q_len)
    if q_len == 0:
      break
    time.sleep(1)

  im = skimage.io.imread(filename)
  conf = channel.basic_publish(exchange=publish_topic,
                        routing_key=publish_topic,
                        body=cPickle.dumps(im))
  print('published.')
  print('confirmation received: %s' % conf)
  # time.sleep(1)
