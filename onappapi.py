import json
from prettytable import PrettyTable
import os, shutil, pycurl
from StringIO import StringIO
from vm import VM
from template import Template

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
        if data:
            return (True, data)
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
        try:
            fd = open(os.path.join(self.tmpdir, url), 'r')
        except:
            return False
        data = fd.read()
        if data: return json.loads(data)
        else: return False

    def exec_url(self, url, method = 'GET'):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, '%s/%s' % (self.url, url))
        c.setopt(c.WRITEDATA, buffer)
        c.setopt(c.USERPWD, '%s:%s' % (self.username, self.password))
        c.setopt(c.CUSTOMREQUEST, method)
        c.perform()
        status = c.getinfo(c.RESPONSE_CODE)
        c.close()

        body = buffer.getvalue()
        if body: body = json.loads(body)

        return { 'status' : status, 'body' : body }

    def is_valid_out(self, output):
        if int(output['status']) in [ 200, 201 ]: return (True, output['body'])
        elif int(output['status']) in [ 404 ]: return (True, output['body']['errors'])
        else: return (False, output['body']['errors'])

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
            print vars(vm)
            return vm

    def vm_browser(self, vm_id):
        vm = self.vm_info(vm_id)
        os.system('x-www-browser http://%s/virtual_machines/%s' % (self.url, vm.identifier))

    def vm_delete(self, vm_id, convert = 0, destroy = 0):
        if convert not in [ 0, 1]: return False
        if destroy not in [ 0, 1]: return False
        data = self.exec_url('virtual_machines/%s.json?convert_last_backup=%s&destroy_all_backups=%s' % ( vm_id, convert, destroy ))
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

    def template_list(self):
        (status, data) = self.get_data('templates/all.json')

        if status:
            pt = PrettyTable(['Label', 'Version', 'OS', 'Virtualitzation'])
            pt.align['Label'] = 'l'
            for tdata in data:
                t = Template(tdata)
                pt.add_row([t.label, t.version, t.operating_system, t.virtualization])

            print pt
