from jsonobj import OnAppJsonObject

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
