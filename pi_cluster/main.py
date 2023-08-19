from utils.jinja_utils import (
    get_templates,
    get_template_from_env,
    load_template_dir,
    create_loader_env,
    render_template_to_file,
)

from jinja2 import Environment, FileSystemLoader

if __name__ == "__main__":
    test_env = {
        "network": {
            "ethernets": [
                {
                    "device": "eth0",
                    "dhcp4": False,
                    "dhcp6": False,
                    "address": "192.168.1.60/24",
                    "gateway": "192.168.1.1",
                    "nameservers": ["192.168.1.1", "1.1.1.1", "1.0.0.1"],
                }
            ]
        },
        "meta": {"ds": {"mode": "local"}, "instance": {"id": "rpi-cl-srv1"}},
        "userdata": {
            "hostname": "rpi-cl-srv1",
            "fqdn": "rpi-cl-srv1.home",
            "manage_hosts": True,
            "ssh_pass_auth": True,
            "ssh_pubkeys": ["ssh-rsa pubkey1", "ssh-rsa pubkey2"],
            "chwpasswd": {
                "expire": False,
                "users": [
                    {
                        "name": "ubuntu",
                        "password": "exPas$word",
                        "type": "hash",
                    }
                ],
            },
            "packages": {
                "update": False,
                "upgrade": False,
                "install": ["curl", "git", "wget", "dos2unix"],
            },
        },
        "users": [
            {
                "default": True,
                "name": "ubuntu",
                "shell": "/bin/bash",
                "passwd": "kjdflojkangloabnlkbgl",
                "lock_passwd": False,
                "groups": ["users", "adm", "sudo"],
                "sudo_str": "ALL=(ALL) NOPASSWD:ALL",
                "ssh_pubkeys": [
                    "ssh-rsa pubkey1",
                    "ssh-rsa pubkey2",
                    "ssh-rsa pubkey3",
                ],
            }
        ],
        "run_cmds": [
            "rm /etc/netplan/50-cloud-init.yaml",
            "netplan generate",
            "netplan apply",
            "localectl set-x11-keymap 'us' pc105",
            "setupcon -k --force || true",
        ],
        "power": {"mode": "reboot"},
        "final_msg": "cloud-init completed.",
    }

    _templates = get_templates("templates/")
    print(f"Templates: {_templates}")

    ## Example: Create a FileSystemLoader to load templates from directory
    #  then create an Environment to load files from with Environment.get_template(file)
    #  Use template.render() with a dict of variables for the template.
    # _loader = FileSystemLoader(searchpath="templates/snippets")
    _loader = load_template_dir(template_dir_path="templates")
    # _env = Environment(loader=_loader)
    _env = create_loader_env(_loader=_loader)

    ## Load network-config template
    _tmpl_net_file = "snippets/tmpl_network-config.j2"
    _net_template = _env.get_template(_tmpl_net_file)

    ## Load meta-data template
    _tmpl_meta_file = "snippets/tmpl_meta-data.j2"
    _meta_template = _env.get_template(_tmpl_meta_file)

    _net_output = _net_template.render(test_env)
    print(f"Render network-config:\n\n{_net_output}")

    _meta_output = _meta_template.render(test_env)
    print(f"Render meta-data:\n\n{_meta_output}")
