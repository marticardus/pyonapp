class OnAppJsonObject(object):
    def __init__(self, json = None, name = None):
        if json and name:
            if name in json:
                json = json[name]

            for name, value in json.items():
                if hasattr(self, name):
                    setattr(self, name, value)

class Log(OnAppJsonObject):
    status = None
    created_at = None
    target_id = None
    updated_at = None
    target_type = None
    action = None
    id = None
    def __init__(self, json = None, name = 'log_item'):
        super(Log, self).__init__(json, name)

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

    def __init__(self, json = None, name = 'data_store'):
        super(DS, self).__init__(json, name)

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

    def __init__(self, json = None, name = 'data_store_group'):
        super(DSZone, self).__init__(json, name)

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

    def __init__(self, json = None, name = 'ip_address'):
        super(IPAddr, self).__init__(json, name)

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

    def __init__(self, json = None, name = 'image_template'):
        super(Template, self).__init__(json, name)

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

    def __init__(self, json = None, name = 'virtual_machine'):
        super(VM, self).__init__(json, name)
        if json:
            if 'virtual_machine' in json:
                json = json['virtual_machine']

            for ip in json['ip_addresses']:
                ip_obj=IPAddr(ip)
