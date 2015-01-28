from jsonobj import OnAppJsonObject

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
