#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys

def usage():
    print '%s resource [action]' % sys.argv[0]
    sys.exit(0)

conf = os.path.join(os.path.expanduser("~"), '.pyonapp.conf')
config = RawConfigParser()

if not os.path.exists(conf):
    config.add_section('onapp')
    config.set('onapp', 'user', raw_input('Username: '))
    config.set('onapp', 'password', raw_input('Passowrd: '))
    config.set('onapp', 'url', raw_input('Hostname: '))
    with open(conf, 'wb') as openconf:
        config.write(openconf)
else:
    config.read(conf)

user = config.get('onapp', 'user')
password = config.get('onapp', 'password')
url = config.get('onapp', 'url')

api = OnApp(user, password, url)

resource = None
action = None

if len(sys.argv) < 2: usage()
if len(sys.argv) >= 2: resource = sys.argv[1]
if len(sys.argv) >= 3: action = sys.argv[2]

if resource == 'vm':
    if action is None or action == 'list':
        api.vm_list()
    elif action == 'info':
        if len(sys.argv) >= 4: vm_id = sys.argv[3]
        else: usage()
        api.vm_info(vm_id)
elif resource == 'template':
    if action is None or action == 'list':
        api.template_list()
