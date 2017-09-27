#!/usr/bin/env python


import time
import sys
import numpy as np
import glob
import skimage
import pika
import cPickle


from skimage.viewer import ImageViewer
from matplotlib import pyplot as plt

topic = sys.argv[1]
print('Listening on topic: %s' % topic)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange=topic,
                         exchange_type='direct')

# result = channel.queue_declare(exclusive=True) # exclusive is required for LVC exchange to work
# queue_name = result.method.queue
queue_name = topic

channel.queue_bind(exchange=topic,
                   queue=queue_name,
                   routing_key=topic)

print(' [*] Waiting for logs. To exit press CTRL+C')

plt.ion()

def display_image(im):
  im = cPickle.loads(im)
  plt.clf()
  plt.imshow(im)
  plt.pause(0.001)
  plt.show(block=False)

# # CHECK LAST MESSAGE
# method_frame, header_frame, body = channel.basic_get(queue=queue_name)
# print(" [lvc] %s" % method_frame)
# if method_frame:
#   display_image(body)

# LISTEN FOR NEW MESSAGES
def callback(ch, method, properties, body):
  print("\n [x] ")
  display_image(body)
  time.sleep(3)
  ch.basic_ack(method.delivery_tag)
  # channel.basic_ack(method.delivery_tag)
  print(" [ack] ")


channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

channel.start_consuming()

