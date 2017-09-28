#!/usr/bin/env python

import requests

user = 'guest'
password = 'guest'


def get_bindings_on_exchange(exchange):
  get_bindings_url = 'http://localhost:15672/api/exchanges/%2f/'+exchange+'/bindings/source'
  # example URL:
  #  http://localhost:15672/api/exchanges/%2f/images/bindings/source
  r = requests.get(get_bindings_url,auth=(user,password))
  bindings = r.json()
  return bindings


# def get_non_exclusive_queues_on_exchange(exchange):
#   bindings = get_bindings_on_exchange(exchange)
#   queues = [binding['destination'] for binding in bindings \
#             if binding['destination_type'] == 'queue' \
#             and 'amq.gen' not in binding['destination']]
#   return queues

def get_queues_on_exchange(exchange):
  bindings = get_bindings_on_exchange(exchange)
  queues = [binding['destination'] for binding in bindings \
            if binding['destination_type'] == 'queue']
  return queues

def get_queue_message_length(queue):
  queue_details_url = 'http://localhost:15672/api/queues/%2f/' + queue
  r = requests.get(queue_details_url,auth=(user,password))
  queue = r.json()
  if 'error' in queue and queue['error'] == 'Object Not Found':
    return 0
  queue_length = queue['messages']
  return queue_length

def get_total_message_count_in_queues(queues):
  total = 0
  for queue in queues: # NOTE: possible parralellization but is the threading overhead not worth it?
    total += get_queue_message_length(queue)
  return total

def get_queued_message_count_on_exchange(exchange):
  queues = get_queues_on_exchange(exchange)
  total = get_total_message_count_in_queues(queues)
  return total

