#!/usr/bin/env python

import numpy as np
import glob
import skimage
import pika
import cPickle


from skimage.viewer import ImageViewer
from matplotlib import pyplot as plt

## SETUP
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='images',
                         exchange_type='x-lvc')

## CHECK FOR LAST MESSAGE CACHED 
result = channel.queue_declare(exclusive=True) # exclusive is required for LVC exchange to work
queue_name = result.method.queue

channel.queue_bind(exchange='images',
                   queue=queue_name,
                   routing_key='images')

method_frame, header_frame, body = channel.basic_get(queue=queue_name)
print(" [lvc] %s" % method_frame)
if method_frame:
  im = cPickle.loads(body)
  plt.clf()
  plt.imshow(im)
  plt.pause(0.001)
  plt.show(block=False)
  # print queue length
  # q = channel.queue_declare(queue_name)
  # q_len = q.method.message_count
  # print('queue length: %s' % q_len)



## SUBSCRIBE AS WORKER BEE

queue_name = 'images'
channel.queue_declare(queue=queue_name)

print queue_name

channel.queue_bind(exchange='images',
                   queue=queue_name,
                   routing_key='images')


print(' [*] Waiting for logs. To exit press CTRL+C')

plt.ion()

def callback(ch, method, properties, body):
    print(" [x] ")
    im = cPickle.loads(body)
    plt.clf()
    plt.imshow(im)
    plt.pause(0.001)
    plt.show(block=False)
    # print queue length
    # q = channel.queue_declare(queue_name)
    # q_len = q.method.message_count
    # print('queue length: %s' % q_len)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()

