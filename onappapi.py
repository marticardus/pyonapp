import json
from prettytable import PrettyTable
import os
import pycurl
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

    def get_data(self, url):
        data = self.get_cache(url)
        if data:
            return data
        else:
            data = self.exec_url(url)
            data = self.is_valid_out(data)
            if data:
                self.write_cache(url, data)
                return data
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
        if output['status'] == 200: return output['body']
        else: return False

    def vm_list(self, sortby = 'Hostname'):
        data = self.get_data('virtual_machines.json')
        if data:
            pt = PrettyTable(['Hostname', 'VMID', 'CPU', 'RAM', 'Disk', 'Powered on'])
            pt.align['Hostname'] = 'l'
            for virtual in data:
                vm = VM(virtual)
                pt.add_row([vm.hostname, vm.id, vm.cpus, vm.memory, vm.total_disk_size, vm.booted])

            print pt.get_string(sortby=sortby)

    def vm_info(self, vm_id):
        data = self.get_data('virtual_machines/%s.json' % vm_id)
        if data:
            vm = VM(data)
            print vars(vm)

    def vm_delete(self, vm_id, convert = 0, destroy = 0):
        if convert not in [ 0, 1]: return False
        if destroy not in [ 0, 1]: return False
        data = self.exec_url('virtual_machines/%s.json?convert_last_backup=%s&destroy_all_backups=%s' % ( vm_id, convert, destroy ))

        if not self.is_valid_out(data):
            print data['body']

    def template_list(self):
        data = self.exec_url('templates/all.json')
        data = self.is_valid_out(data)

        if data:
            pt = PrettyTable(['Label', 'Version', 'OS', 'Virtualitzation'])
            pt.align['Label'] = 'l'
            for tdata in data:
                t = Template(tdata)
                pt.add_row([t.label, t.version, t.operating_system, t.virtualization])

            print pt
