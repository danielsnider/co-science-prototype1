import sys
import requests

user = 'guest'
password = 'guest'

exchange_of_interest = sys.argv[1]
if not exchange_of_interest:
  print('error')
  sys.exit(1)

get_exchange_bindings_url = 'http://localhost:15672/api/exchanges/%2f/'+exchange_of_interest+'/bindings/source'
r = requests.get(get_exchange_bindings_url,auth=(user,password))
exchange_bindings = r.json()

queues = [binding['destination'] for binding in exchange_bindings if binding['destination_type'] == 'queue']

if not queues:
  print('%s has no binded queues' % exchange_of_interest)

for queue_name in queues:
  queue_details_url = 'http://localhost:15672/api/queues/%2f/' + queue_name
  r = requests.get(queue_details_url,auth=(user,password))
  queue = r.json()
  print('\nQUEUE COUNT SUMMARY: %s' % queue_name)
  print('message_stats: %s' % queue['message_stats'])
  print('messages: %s' % queue['messages'])
  print('messages_details: %s' % queue['messages_details'])
  print('messages_paged_out: %s' % queue['messages_paged_out'])
  print('messages_persistent: %s' % queue['messages_persistent'])
  print('messages_ram: %s' % queue['messages_ram'])
  print('messages_ready: %s' % queue['messages_ready'])
  print('messages_ready_details: %s' % queue['messages_ready_details'])
  print('messages_ready_ram: %s' % queue['messages_ready_ram'])
  print('messages_unacknowledged: %s' % queue['messages_unacknowledged'])
  print('messages_unacknowledged_details: %s' % queue['messages_unacknowledged_details'])
  print('messages_unacknowledged_ram: %s' % queue['messages_unacknowledged_ram'])


