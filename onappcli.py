#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys
args = sys.argv
cmd = os.path.basename(args.pop(0))

def usage(resource = None):
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
        elif resource == 'cache':
            print '%s cache clear' % cmd
    else:
        print '%s resource action' % cmd
        print 'Available resources: vm, template, cache'

    sys.exit(0)

conf = os.path.join(os.path.expanduser("~"), '.pyonapp.conf')
config = RawConfigParser()

if not os.path.exists(conf):
    config.add_section('onapp')
    config.set('onapp', 'user', raw_input('Username: '))
    config.set('onapp', 'password', raw_input('Passowrd: '))
    config.set('onapp', 'url', raw_input('Hostname: '))
    with open(conf, 'wb') as openconf: config.write(openconf)
else: config.read(conf)

user = config.get('onapp', 'user')
password = config.get('onapp', 'password')
url = config.get('onapp', 'url')

api = OnApp(user, password, url)

resource = None
action = None

if len(args) > 0: resource = args.pop(0)
if len(args) > 0: action = args.pop(0)

if resource == 'vm':
    if  action == 'list':
        api.vm_list()
    elif action == 'info':
        if len(args) > 0: vm_id = args.pop(0)
        else: usage()
        api.vm_info(vm_id)
    elif action == 'start':
        if len(args) > 0: vm_id = args.pop(0)
        else: usage()
        api.vm_start(vm_id)
    elif action == 'stop':
        if len(args) > 0: vm_id = args.pop(0)
        else: usage()
        api.vm_stop(vm_id)
    elif action == 'shutdown':
        if len(args) > 0: vm_id = args.pop(0)
        else: usage()
        api.vm_shutdown(vm_id)
    else: usage('vm')

elif resource == 'template':
    if action == 'list':
        api.template_list()
    else: usage('template')
elif resource == 'cache':
    if action == 'clear':
        api.clear_cache()
    else: usage('cache')
else: usage()
