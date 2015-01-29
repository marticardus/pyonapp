#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys

def get_arg(resource = None):
    if len(sys.argv) > 0: return sys.argv.pop(0)
    else: usage(resource)

cmd = get_arg()

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

resource = get_arg()
if resource: action = get_arg(resource)

if resource == 'vm':
    if  action == 'list':
        api.vm_list()
    elif action == 'info':
        vm_id = get_arg(resource)
        api.vm_info(vm_id)
    elif action == 'browser':
        vm_id = get_arg(resource)
        api.vm_browser(vm_id)
    elif action == 'start':
        vm_id = get_arg(resource)
        api.vm_start(vm_id)
    elif action == 'stop':
        vm_id = get_arg(resource)
        api.vm_stop(vm_id)
    elif action == 'shutdown':
        vm_id = get_arg(resource)
        api.vm_shutdown(vm_id)
    elif action == 'delete':
        vm_id = get_arg(resource)
        api.vm_delete(vm_id)
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
