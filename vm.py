from jsonobj import OnAppJsonObject
from ipaddr import IPAddr

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
