#!/usr/bin/env python

import pika
import cPickle
import numpy as np
import glob
import skimage
import time

from skimage.viewer import ImageViewer
from matplotlib import pyplot as plt


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='images',
                         exchange_type='direct')


for filename in glob.iglob('./images/*'):
  print('%s' % filename)
  im = skimage.io.imread(filename)
  channel.basic_publish(exchange='images',
                        routing_key='images',
                        body=cPickle.dumps(im))
  time.sleep(2)
