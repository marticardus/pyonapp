import json, time
from prettytable import PrettyTable
import os, shutil, pycurl, sys
from StringIO import StringIO 

# Objects
from resources import VM, Template, DSZone, DS, Log, Usage, Disk, DiskUsage

class OnApp(object):
    username = None
    password = None
    url = None
    tmpdir = '/tmp/onapp'

    def __init__(self, username, password, url, tmpdir = '/tmp/onapp'):
        self.username = username
        self.password = password
        self.url = url

    def clear_cache(self):
        shutil.rmtree(self.tmpdir)

    def get_data(self, url):
        data = self.get_cache(url)
        if data: return (True, data)
        else:
            data = self.exec_url(url)
            (status, data) = self.is_valid_out(data)
            if status:
                self.write_cache(url, data)
                return (status, data)
        return False

    def write_cache(self, url, data):
        fullpath = os.path.join(self.tmpdir, url)
        if not os.path.exists(os.path.dirname(fullpath)): os.makedirs(os.path.dirname(fullpath))
        fd = open(fullpath, 'w')
        fd.write(json.dumps(data, indent=3))
        fd.close()

    def get_cache(self, url):
        if os.path.isfile(os.path.join(self.tmpdir, url)):
            ago=time.time()-300
            if os.path.getmtime(os.path.join(self.tmpdir, url))<ago:
                return False
        try:
            fd = open(os.path.join(self.tmpdir, url), 'r')
        except:
            return False
        data = fd.read()
        if data: return json.loads(data)
        else: return False

    def exec_url(self, url, method = 'GET', data = None):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, '%s/%s' % (self.url, url))
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.USERPWD, '%s:%s' % (self.username, self.password))
        c.setopt(c.CUSTOMREQUEST, method)
        c.setopt(c.HTTPHEADER, ['Accept: application/json', 'Content-type: application/json'])
        if json:
            c.setopt(c.POSTFIELDS, json.dumps(data))
        c.perform()
        status = c.getinfo(c.RESPONSE_CODE)
        c.close()

        body = buffer.getvalue()
        if body: body = json.loads(body)

        return { 'status' : status, 'body' : body }

    def is_valid_out(self, output):
        if int(output['status']) in [ 200, 201, 204 ]:
            if int(output['status']) == 204: return 'OK'
            return (True, output['body'])
        elif int(output['status']) in [ 403, 404, 422, 500 ]: 
            for d in output['body']['errors']: print d
            sys.exit(1)
        else: return (False, output['body']['errors'])

    def log_list(self):
        (status, data) = self.get_data('logs.json')
        if status:
            pt = PrettyTable([ 'ID', 'Action', 'Status', 'Target' ])
            for d in data:
                l = Log(d)
                pt.add_row([ l.id, l.action, l.status, '%s #%s' % (l.target_type, l.target_id) ])

            print pt

    def log_info(self, log_id):
        (status, data) = self.get_data('logs/%s.json' % log_id)
        if status:
            l = Log(data)
            print vars(l)

    def vm_list(self, sortby = 'Hostname'):
        (status, data) = self.get_data('virtual_machines.json')
        if status:
            pt = PrettyTable(['Hostname', 'VMID', 'Identifier', 'CPU', 'RAM', 'Disk', 'Power'])
            pt.align['Hostname'] = 'l'
            for virtual in data:
                vm = VM(virtual)
                pt.add_row([vm.hostname, vm.id, vm.identifier, vm.cpus, vm.memory, vm.total_disk_size, 'On' if vm.booted else 'Off' ])

            print pt.get_string(sortby=sortby)

    def vm_info(self, vm_id):
        (status, data) = self.get_data('virtual_machines/%s.json' % vm_id)
        if status:
            vm = VM(data)
            return vm

    def vm_browser(self, vm_id):
        vm = self.vm_info(vm_id)
        os.system('x-www-browser http://%s/virtual_machines/%s' % (self.url, vm.identifier))

    def vm_delete(self, vm_id, convert = 0, destroy = 0):
        if convert not in [ 0, 1]: return False
        if destroy not in [ 0, 1]: return False
        data = self.exec_url('virtual_machines/%s.json?convert_last_backup=%s&destroy_all_backups=%s' % ( vm_id, convert, destroy ), 'DELETE')
        (status, data) = self.is_valid_out(data)
        if isinstance(data, list):
            for d in data:
                print d
        else:
            print data

    def vm_start(self, vm_id):
        data = self.exec_url('virtual_machines/%s/startup.json' % vm_id, 'POST')
        (status, data) = self.is_valid_out(data)
        print data
        
    def vm_shutdown(self, vm_id):
        data = self.exec_url('virtual_machines/%s/shutdown.json' % vm_id, 'POST')
        (status, data) = self.is_valid_out(data)
        print data

    def vm_stop(self, vm_id):
        data = self.exec_url('virtual_machines/%s/stop.json' % vm_id, 'POST')
        (status, data) = self.is_valid_out(data)
        print data

    def vm_create(self, **kwargs):
        args = {}
        for (item, value) in kwargs.items():
            args[item] = value
        vs = { 'virtual_machine' : args }

        data = self.exec_url('virtual_machines.json', 'POST', vs)
        (status, data) = self.is_valid_out(data)
        if isinstance(data, list):
            for d in data: print d
        else: return VM(data)

    def template_list(self, types = 'all', user_id = None):
        if types in [ 'all', 'own', 'user', 'inactive' ]:
            (status, data) = self.get_data('templates/%s.json' % types)
        elif types == 'system':
            (status, data) = self.get_data('templates.json')
        elif types == 'userid':
            if not user_id: return False
            (status, data) = self.get_data('templates/user/%s.json' % user_id)

        if status:
            pt = PrettyTable(['Label', 'ID', 'Version', 'OS', 'Virtualitzation'])
            pt.align['Label'] = 'l'
            for tdata in data:
                t = Template(tdata)
                pt.add_row([t.label, t.id, t.version, t.operating_system, t.virtualization])

            print pt

    def dszone_list(self):
        (status, data) = self.get_data('settings/data_store_zones.json')

        if status:
            pt = PrettyTable(['Label', 'ID'])
            pt.align['Label'] = 'l'
            for tdata in data:
                z = DSZone(tdata)
                pt.add_row([z.label, z.id])

            print pt

    def ds_list(self):
        (status, data) = self.get_data('settings/data_stores.json')

        if status:
            pt = PrettyTable(['Label', 'ID', 'identifier', 'usage', 'Enabled' ])
            pt.align['Label'] = 'l'
            for ds in data:
                d = DS(ds)
                pt.add_row([d.label, d.id, d.identifier, d.usage, d.enabled ])

            print pt

    def alerts(self):
        (status, data) = self.get_data('alerts.json')
        if status:
            print 'zombie_data_stores: %s ' % data['alerts']['zombie_data_stores']
            print 'zombie_disks: %s ' % data['alerts']['zombie_disks']
            print 'zombie_domains: %s ' % data['alerts']['zombie_domains']
            print 'zombie_transactions: %s ' % data['alerts']['zombie_transactions']

    def onapp_version(self):
        (status, data) = self.get_data('version.json')
        if status: print "OnApp Version: %s" % data['version']

    def usage(self):
        (status, data) = self.get_data('usage_statistics.json')
        if status:
            pt = PrettyTable([ 'User ID', 'VS ID', 'CPU Used', 'Disk reads', 'Disk writes', 'Data read', 'Data written', 'BW Sent', 'BW Received' ])
            pt.align['User ID'] = 'l'
            pt.align['VS ID'] = 'l'
            pt.align['CPU Used'] = 'r'
            pt.align['Disk reads'] = 'r'
            pt.align['Disk writes'] = 'r'
            pt.align['Data read'] = 'r'
            pt.align['Data written'] = 'r'
            pt.align['BW Sent'] = 'r'
            pt.align['BW Received'] = 'r'
            for d in data:
                u = Usage(d)
                pt.add_row([ u.user_id, u.virtual_machine_id, u.cpu_usage, u.reads_completed, u.writes_completed, u.data_read, u.data_written, u.data_sent, u.data_received ])
            print pt

    def disk_list(self, data = None):
        if not data: (status, data) = self.get_data('settings/disks.json')
        else: (status, data) = data
        if status:
            pt = PrettyTable([ 'ID', 'Label', 'Size', 'Data Store', 'VS', 'FS', 'Type', 'Mounted', 'Built', 'Auto-Backup' ])
            for da in data:
                d = Disk(da)
                if d.primary: 
                    disktype = 'Primary'
                    mounted = 'Yes'
                elif d.is_swap: 
                    disktype = 'Swap'
                    mounted = 'Yes'
                elif d.mount_point: 
                    disktype = 'Secondary'
                    mounted = 'Yes'
                else: 
                    disktype = 'Unknown'
                    disktype = 'No'
                pt.add_row( [ d.id, d.label, '%s GB' % d.disk_size, d.data_store_id, d.virtual_machine_id, d.file_system, disktype, mounted, 'Yes' if d.built else 'No', 'Yes' if d.has_autobackups  else 'No' ])

            print pt

    def disk_usage(self, disk_id):
        (status, data) = self.get_data('settings/disks/%s/usage.json' % disk_id)
        if status: 
            pt = PrettyTable(['User ID', 'VS ID', 'Disk ID', 'Data Read', 'Data Written', 'Reads completed', 'Writes completed', 'Stat Time' ])
            for d in data:
                du = DiskUsage(d)
                pt.add_row( [ du.user_id, du.virtual_machine_id, du.disk_id, du.data_read, du.data_written, du.reads_completed, du.writes_completed, du.stat_time ] )

            print pt
                
    def disk_list_vs(self, vm_id):
        self.disk_list(data = self.get_data('virtual_machines/%s/disks.json' % vm_id))

    def disk_create(self, vm_id, data_store_id, label, primary, disk_size, is_swap, mount_point, hot_attach, min_iops, add_to_linux_fstab, add_to_freebsd_fstab, require_format_disk, file_system):
        disk = {
                'primary' : primary,
                'disk_size' : disk_size,
                'file_system' : file_system,
                'data_store_id' : data_store_id,
                'label' : label,
                'require_format_disk' : require_format_disk,
                'mount_point' : mount_point,
                'hot_attach' : hot_attach,
                'min_iops' : min_iops,
                'add_to_linux_fstab' : add_to_linux_fstab,
                'add_to_freebsd_fstab' : add_to_freebsd_fstab
                }
        data = self.exec_url('virtual_machines/%s/disks.json' % vm_id, 'POST', { 'disk' : disk })
        (status, data) = self.is_valid_out(data)
        if status:
            disk = Disk(data)
            print vars(disk)

    def disk_delete(self, vm_id, disk_id):
        (status, data) = self.exec_url('virtual_machines/%s/disks/%s.json' % (vm_id, disk_id), 'DELETE')
        if status: print 'OK'

