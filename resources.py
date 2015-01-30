class OnAppJsonObject(object):
    api = None
    def __init__(self, jsondata = None, name = None, api = None):
        self.api = api
        if jsondata and name:
            if name in jsondata:
                jsondata = jsondata[name]

            for name, value in jsondata.items():
                if hasattr(self, name):
                    setattr(self, name, value)

class DiskUsage(OnAppJsonObject):
    disk_id = None
    created_at = None
    updated_at = None
    data_read = None
    data_written = None
    stat_time = None
    writes_completed = None
    reads_completed = None
    user_id = None
    virtual_machine_id = None

    def __init__(self, jsondata = None, name = 'disk_hourly_stat'):
        super(DiskUsage, self).__init__(jsondata, name)
        if self.data_read: self.data_read = u'%.2f' % float((float(self.data_read) / 1024) / 3600)
        if self.data_written: self.data_written = u'%.2f' % float((float(self.data_written) / 1024) / 3600)

class Disk(OnAppJsonObject):
    primary = None
    virtual_machine_id = None
    has_autobackups = None
    id = None
    mount_point = None
    built = None
    label = None
    max_iops = None
    burst_iops = None
    is_swap = None
    add_to_linux_fstab = None
    disk_vm_number = None
    burst_bw = None
    data_store_id = None
    updated_at = None
    max_bw = None
    volume_id = None
    disk_size = None
    min_iops = None
    file_system = None
    locked = None
    created_at = None
    add_to_freebsd_fstab = None
    iqn = None
    identifier = None

    vm = None

    def __init__(self, jsondata = None, name = 'disk', api = None):
        super(Disk, self).__init__(jsondata, name, api)

        if self.api:
            if self.virtual_machine_id:
                self.vm = api.vm_info(self.virtual_machine_id)

class Usage(OnAppJsonObject):
    cpu_usage = None
    user_id = None
    writes_completed = None
    data_received = None
    data_sent = None
    data_read = None
    virtual_machine_id = None
    reads_completed = None
    data_written = None

    def __init__(self, jsondata = None, name = 'vm_stat'):
        super(Usage, self).__init__(jsondata, name)

class Log(OnAppJsonObject):
    status = None
    created_at = None
    target_id = None
    updated_at = None
    target_type = None
    action = None
    id = None
    def __init__(self, jsondata = None, name = 'log_item'):
        super(Log, self).__init__(jsondata, name)

class DS(OnAppJsonObject):
    data_store_group_id = None
    data_store_size = None
    created_at = None
    enabled = None
    updated_at = None
    label = None
    zombie_disks_size = None
    hypervisor_group_id = None
    data_store_type = None
    ip = None
    usage = None
    identifier = None
    local_hypervisor_id = None
    id = None
    iscsi_ip = None

    def __init__(self, jsondata = None, name = 'data_store'):
        super(DS, self).__init__(jsondata, name)

class DSZone(OnAppJsonObject):
    default_max_iops = None
    min_disk_size = None
    created_at = None
    updated_at = None
    default_burst_iops = None
    label = None
    federation_enabled = None
    federation_id = None
    closed = None
    location_group_id = None
    traded = None
    id = None

    def __init__(self, jsondata = None, name = 'data_store_group'):
        super(DSZone, self).__init__(jsondata, name)

class IPAddr(OnAppJsonObject):
    address = None
    broadcast = None
    created_at = None
    customer_network_id = None
    disallowed_primary = False
    free = False
    gateway = None
    hypervisor_id = None
    id = None
    ip_address_pool_id = None
    netmask = None
    network_address = None
    network_id = None
    pxe = None
    updated_at = None
    user_id = None

    def __init__(self, jsondata = None, name = 'ip_address'):
        super(IPAddr, self).__init__(jsondata, name)

class Template(OnAppJsonObject):
    file_name = None
    cdn = None
    updated_at = None
    template_size = None
    virtualization = None
    operating_system_arch = None
    id = None
    ext4 = None
    disk_target_device = None
    operating_system_edition = None
    remote_id = None
    allow_resize_without_reboot = None
    label = None
    parent_template_id = None
    state = None
    version = None
    manager_id = None
    baremetal_server = None
    initial_password = None
    operating_system_tail = None
    smart_server = None
    min_memory_size = None
    operating_system_distro = None
    min_disk_size = None
    operating_system = None
    user_id = None
    backup_server_id = None
    checksum = None
    created_at = None
    resize_without_reboot_policy = None
    allowed_hot_migrate = None
    allowed_swap = None
    initial_username = None

    def __init__(self, jsondata = None, name = 'image_template'):
        super(Template, self).__init__(jsondata, name)

class VM(OnAppJsonObject):
    preferred_hvs = []
    remote_access_password = None
    recovery_mode = None
    suspended = None
    cpu_priority = None
    updated_at = None
    ip_addresses = []
    cpus = None
    add_to_marketplace = None
    vip = None
    initial_root_password_encrypted = None
    local_remote_access_ip_address = None
    total_disk_size = None
    deleted_at = None
    id = None
    cpu_sockets = None
    support_incremental_backups = None
    template_label = None
    operating_system_distro = None
    built = None
    hostname = None
    price_per_hour_powered_off = None
    enable_autoscale = None
    allow_resize_without_reboot = None
    label = None
    note = None
    state = None
    local_remote_access_port = None
    memory = None
    monthly_bandwidth_used = None
    price_per_hour = None
    initial_root_password = None
    storage_server_type = None
    admin_note = None
    hypervisor_id = None
    enable_monitis = None
    strict_virtual_machine_id = None
    cpu_threads = None
    user_id = None
    edge_server_type = None
    min_disk_size = None
    customer_network_id = None
    operating_system = None
    locked = None
    service_password = None
    created_at = None
    firewall_notrack = None
    allowed_hot_migrate = None
    allowed_swap = None
    xen_id = None
    booted = None
    cpu_units = None
    identifier = None
    template_id = None
    cpu_shares = None

    def __init__(self, jsondata = None, name = 'virtual_machine'):
        super(VM, self).__init__(jsondata, name)
        if jsondata:
            if 'virtual_machine' in jsondata:
                jsondata = jsondata['virtual_machine']

            for ip in jsondata['ip_addresses']:
                ip_obj=IPAddr(ip)
