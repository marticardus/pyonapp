#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys

def usage(resource = None):
    cmd = os.path.basename(sys.argv[0])
    if resource:
        if resource == 'vm':
            print '%s vm action' % cmd
            print 'Available actions: list, info, start, stop, shutdown, delete'
            print 'Example:'
            print '\t%s shutdown 45' % cmd
            print '\t%s start 45' % cmd
        elif resource == 'template':
            print '%s template action' % cmd
            print 'Available actions: list'
    else:
        print '%s resource action' % cmd
        print 'Available resources: vm, template'

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
    if  action == 'list':
        api.vm_list()
    elif action == 'info':
        if len(sys.argv) >= 4: vm_id = sys.argv[3]
        else: usage()
        api.vm_info(vm_id)
    elif action == 'start':
        if len(sys.argv) >= 4: vm_id = sys.argv[3]
        else: usage()
        api.vm_start(vm_id)
    elif action == 'stop':
        if len(sys.argv) >= 4: vm_id = sys.argv[3]
        else: usage()
        api.vm_stop(vm_id)
    elif action == 'shutdown':
        if len(sys.argv) >= 4: vm_id = sys.argv[3]
        else: usage()
        api.vm_shutdown(vm_id)
    else:
        usage('vm')

elif resource == 'template':
    if action == 'list':
        api.template_list()
    else:
        usage('template')
