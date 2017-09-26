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

channel.exchange_declare(exchange='images',
                         exchange_type='direct')

channel.queue_declare(queue='images')

channel.queue_bind(exchange='images',
                   queue='images',
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

channel.basic_consume(callback,
                      queue='images',
                      no_ack=True)

channel.start_consuming()

