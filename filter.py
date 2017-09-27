#!/usr/bin/env python

import numpy as np
import glob
import skimage
import pika
import cPickle


from skimage.viewer import ImageViewer
from matplotlib import pyplot as plt

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

subscribe_topic = 'images-d'
channel.exchange_declare(exchange=subscribe_topic,
                         exchange_type='direct')

result = channel.queue_declare(exclusive=True) # exclusive is required for LVC exchange to work
queue_name = result.method.queue

channel.queue_bind(exchange=subscribe_topic,
                   queue=queue_name,
                   routing_key=subscribe_topic)

print(' [*] Waiting for logs. To exit press CTRL+C')

plt.ion()

#publish
publish_topic = 'filter'
channel.exchange_declare(exchange=publish_topic,
                         exchange_type='x-lvc')

def filter_image(im):
  im = cPickle.loads(im)
  im2 = skimage.filters.gaussian(im)
  channel.basic_publish(exchange=publish_topic,
                        routing_key=publish_topic,
                        body=cPickle.dumps(im2))

# # CHECK LAST MESSAGE
# method_frame, header_frame, body = channel.basic_get(queue=queue_name)
# print(" [lvc] %s" % method_frame)
# if method_frame:
#   filter_image(body)

# LISTEN FOR NEW MESSAGES
def callback(ch, method, properties, body):
    print(" [ filtered x] ")
    filter_image(body)
    # from IPython import embed

    # embed() # drop into an IPython session
    # channel.confirm_delivery()
    # ch.basic_ack(method.delivery_tag)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=False)

channel.start_consuming()

