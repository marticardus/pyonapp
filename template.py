from jsonobj import OnAppJsonObject

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
