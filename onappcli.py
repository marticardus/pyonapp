#!/usr/bin/python
from ConfigParser import RawConfigParser
from onappapi import OnApp
import os, sys, argparse, json

def get_arg(resource = None, exit = True):
    if len(sys.argv) > 0: return sys.argv.pop(0)
    else: 
        if exit: usage(resource)
        else: return None

cmd = os.path.basename(get_arg())

def usage(resource = None):
    info = {
            'vm' : { 'actions' : [ 'list', 'info', 'start', 'stop', 'shutdown', 'delete' ], 'example' : [ 'start 45', 'shutdown 45' ] },
            'template' : { 'actions' : [ 'list', 'listall', 'listsystem', 'listown', 'listinactive', 'listuser', 'listuserid [user_id]' ] },
            'cache' : { 'actions' : [ 'clear '] },
            'ds' : { 'actions' : [ 'list' ] },
            'dszone' : { 'actions' : [ 'list' ] },
            'log' : { 'actions' : [ 'list', 'info [log_id]' ] },
            'system' : { 'actions' : [ 'alerts', 'version' ] },
            'usage' : { 'actions' : [ 'all' ] },
            'disk' : { 'actions' : [ 'list', 'list vs [vm_id]' ] },
            }
    if resource:
        if resource in info:
            print '%s %s action' % (cmd, resource)
            print 'Available actions: %s' % ', '.join(info[resource]['actions'])
            if 'example' in info[resource]:
                for e in info[resource]['example']:
                    print '\t%s %s %s' % (cmd, resource, e)
    else:
        print '%s resource action' % cmd
        print 'Available resources: %s' % ', '.join(info.keys())
    sys.exit(0)

def cliparser(prog, args):
    parser = argparse.ArgumentParser(prog=prog)
    for arg in args:
#        required = arg['required'] if 'required' in arg else False
#        type = arg['type'] if 'type' in arg else str
#        default = arg['default'] if 'default' in arg else None
        #parser.add_argument('--%s' % arg['arg'], help=arg['help'], required = required, type = type, default = default)
        if 'options' in arg: parser.add_argument(arg['args'], **arg['options'])
        else: parser.add_argument(arg['args'])
    return vars(parser.parse_args([] if len(sys.argv) == 0 else sys.argv))


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
    elif action == 'create':
        parser = argparse.ArgumentParser(prog='onappcli vm create')
        parser.add_argument('--memory', help='Max Memory', dest='memory', required = True, type = int)
        parser.add_argument('--cpus', help='Max CPU', dest='cpus', required = True, type = int)
        parser.add_argument('--cpu_shares', help='CPU Shares', dest='cpu_shares', default = 100, type = int)
        parser.add_argument('--cpu-sockets', help='CPU Sockets', dest='cpu_sockets', default = 1, type = int)
        parser.add_argument('--cpu-threads', help='CPU Threads', dest='cpu_threads', default = 1, type = int)
        parser.add_argument('--hostname', help='Set hostname', dest='hostname', required = True, type = str)
        parser.add_argument('--label', help='Set label', dest='label', required = True, type = str)
        parser.add_argument('--data-store-group-primary-id', help='Primary Datastore ID', required = True, type = int)
        parser.add_argument('--primary-disk-size', help='Set primary disk size', dest='primary_disk_size', default = 5, type = int)
        parser.add_argument('--primary-disk-min-iops', help='Primary disk IOPS', dest='primary_disk_min_iops', default = 100, type = int)
        parser.add_argument('--data-store-group-swap-id', help='Swap Datastore ID', default = 1, type = int)
        parser.add_argument('--swap-disk-size', help='Set swap disk size', dest='swap_disk_size', default = 0, type = int)
        parser.add_argument('--swap-disk-min-iops', help='Swap disk IOPS', dest='swap_disk_min_iops', default = 100, type = int)
        parser.add_argument('--primary-network-group-id', help='Network zone', dest='primary_network_group_id', required = True, type = int)
        parser.add_argument('--primary-network-id', help='Set primary network id', dest='primary_network_id', required = True, type = int)
        parser.add_argument('--selected-ip-address-id', help='Primary IP address ID', dest='selected_ip_address_id', default = 0, type = int)
        parser.add_argument('--required-virtual-machine-build', help='Build virtual machine', dest='required_virtual_machine_build', default=1, type = int)
        parser.add_argument('--required-virtual-machine-startup', help='Start after create', dest='required_virtual_machine_startup', default = 1, type = int)
        parser.add_argument('--required-ip-address-assignment', help='Auto assing IP', dest='required_ip_address_assignment', default = 1, type = int)
        parser.add_argument('--required-automatic-backup', help='Auto backups', dest='required_automatic_backup', default = 0, type = int)
        parser.add_argument('--type-of-format', help='Type of disk format', dest='type_of_format', default = 'ext4', type = str)
        parser.add_argument('--enable-autoscale', help='Enable autoscale', dest='enable_autoscale', default = 0, type = int)
        parser.add_argument('--recipe-ids', help='Recipe IDs', dest='recipe_ids', default = [], type = list)
        parser.add_argument('--custom-recipe-variables', help='Custom recipe variables', default = [], type = list)
        parser.add_argument('--template-id', help='Template ID', dest='template_id', required = True, type = int)
        parser.add_argument('--initial-root-password', help='Root password', dest='initial_root_password', required = False, type = str)
        parser.add_argument('--rate-limit', help='Rate limit', dest='rate_limit', default = 'none', type = str)
        parser.add_argument('--hypervisor-group-id', help='Hypervisor group id', dest='hypervisor_group_id', type = int)
        parser.add_argument('--hypervisor-id', help='Hypervisor', dest='hypervisor_id', required = True, type = int)
        parser.add_argument('--licensing-server-id', help='Licensing server', dest='licensing_server_id', default = 0, type = int)
        parser.add_argument('--licensing-type', help='License type', dest='licensing_type', default = 'kms', type = str)
        parser.add_argument('--licensing-key', help='License Key', dest='licensing_key', default = '', type = str)

        args = vars(parser.parse_args([] if len(sys.argv) == 0 else sys.argv))
        vm = api.vm_create(**args)
        if vm and vm.__class__.__name__ == 'VM':
            print vm.id
            print vm.label
            print vm.hostname

    else: usage('vm')

elif resource == 'template':
    if action == 'list' or action == 'listall': api.template_list('all')
    elif action == 'listsystem': api.template_list('system')
    elif action == 'listown': api.template_list('own')
    elif action == 'listuser': api.template_list('user')
    elif action == 'listinactive': api.template_list('inactive')
    elif action == 'listuserid': 
        user = get_arg('template')
        api.template_list('user', user)
    else: usage('template')
elif resource == 'cache':
    if action == 'clear':
        api.clear_cache()
    else: usage('cache')
elif resource == 'dszone':
    if action == 'list':
        api.dszone_list()
    else: usage('dszone')
elif resource == 'ds':
    if action == 'list':
        api.ds_list()
    else: usage('ds')
elif resource == 'log':
    if action == 'list': api.log_list()
    elif action == 'info': api.log_info(get_arg('log'))
    else: usage('log')
elif resource == 'system':
    if action == 'alerts': api.alerts()
    elif action == 'version': api.onapp_version()
    else: usage('system')
elif resource == 'usage':
    if action == 'all': api.usage()
    else: usage('usage')
elif resource == 'disk':
    if action == 'list': 
        subaction = get_arg('disk', False)
        if not subaction: api.disk_list()
        elif subaction == 'vs': api.disk_list_vs( vm_id = get_arg('disk'))
        else: usage('disk')
    elif action == 'usage': api.disk_usage( disk_id = get_arg('disk'))
    elif action == 'create':
        list_args = [
                { 'args' : '--vs-id',                   'options' : { 'required' : True, 'type' : int,   'dest' : 'vm_id' } },
                { 'args' : '--data-store-id',           'options' : { 'required' : True, 'type' : int,   'dest' : 'data_store_id' } }, 
                { 'args' : '--label',                   'options' : { 'required' : True, 'type' : str, } },
                { 'args' : '--primary',                 'options' : { 'required' : True, 'type' : str,   'default' : 'false', 'choices' : [ 'true', 'false' ] } },
                { 'args' : '--disk_size',               'options' : { 'required' : True, 'type' : int,   'dest' : 'disk_size' }},
                { 'args' : '--is-swap',                 'options' : { 'required' : True, 'type' : str,   'dest' : 'is_swap', 'choices' : [ 'true', 'false' ] } },
                { 'args' : '--mount-point',             'options' : { 'required' : False,'type' : str,   'dest' : 'mount_point' } },
                { 'args' : '--hot-attach',              'options' : { 'default' : True,  'type' : bool,  'dest' : 'hot_attach'  } },
                { 'args' : '--min-iops',                'options' : { 'default' : 100,   'type' : int,   'dest' : 'min_iops' } },
                { 'args' : '--add-to-linux-fstab',      'options' : { 'default' : False, 'type' : bool,  'dest' : 'add_to_linux_fstab' } },
                { 'args' : '--add-to-freebsd-fstab',    'options' : { 'default' : False, 'type' : bool,  'dest' : 'add_to_freebsd_fstab' } },
                { 'args' : '--require-format-disk',     'options' : { 'default' : False, 'type' : str,   'dest' : 'require_format_disk', 'choices' : [ 'true', 'false' ] } },
                { 'args' : '--file-system',             'options' : { 'required' : True, 'type' : str,   'dest' : 'file_system', 'choices' : [ 'ext3', 'ext4' ] } },
                ]
        args = cliparser(prog='onappcli disk create', args = list_args)
        api.disk_create(**args)
    elif action == 'delete': 
        list_args = [
                { 'args' : '--vs-id',   'options' : { 'required' : True, 'type' : int,   'dest' : 'vm_id' } },
                { 'args' : '--disk-id', 'options' : { 'required' : True, 'type' : int,   'dest' : 'disk_id' } },
                ]
        args = cliparser(prog='onappcli disk delete', args = list_args)
        api.disk_delete(**args)
    else: usage('disk')
else: usage()
