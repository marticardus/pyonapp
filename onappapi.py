import json
import pycurl
from StringIO import StringIO
from vm import VM
from template import Template

class OnApp(object):
    username = None
    password = None
    url = None

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url

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

    def vm_list(self):
        data = self.exec_url('virtual_machines.json')
        data = self.is_valid_out(data)
        if data:
            for virtual in data:
                vm = virtual['virtual_machine']

                vm_id = vm['id']
                vm_name = vm['hostname']

                print "id: %s\t\thostname: %s" % (vm_id, vm_name)

    def vm_info(self, vm_id):
        data = self.exec_url('virtual_machines/%s.json' % vm_id)
        data = self.is_valid_out(data)
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
            for t in data:
                print vars(Template(t))
