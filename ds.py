from jsonobj import OnAppJsonObject

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
