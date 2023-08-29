from __future__ import annotations

from pathlib import Path

from loguru import logger as log

export_dir: Path = Path("export")
scripts_export_dir: Path = Path(f"{export_dir}/scripts")

templates_dir: str = "templates"
hashi_up_templates_dir: str = f"{templates_dir}/hashi-up"
hashi_server_templates_dir: str = f"{hashi_up_templates_dir}/server"
hashi_agent_templates_dir: str = f"{hashi_up_templates_dir}/agent"

hashi_cluster_privkey: str = (
    "../ansible/roles/security/hashi-ssh-setup/files/hashi-pi_id_rsa"
)
host_privkey: Path = Path("~/.ssh/hashi-pi_id_rsa").expanduser()
hashi_cluster_pubkey: str = (
    "../ansible/roles/security/hashi-ssh-setup/files/hashi-pi_id_rsa.pub"
)
host_pubkey: Path = Path("~/.ssh/hashi-pi_id_rsa.pub").expanduser()

## Allowed types for HashiTemplate class instances
valid_template_types: list[str] = ["server", "agent", "nomad_job"]

retry_join_ips: list[str] = ["192.168.1.60"]

## Server 1 Consul
server1_consul_template_dict = {
    "template_name": "Server 1 Consul",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_consul.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.60",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 1,
}

## Server 2 Consul
server2_consul_template_dict = {
    "template_name": "Server 2 Consul",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_consul.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.60",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 3,
}

## Server 3 Consul
server3_consul_template_dict = {
    "template_name": "Server 3 Consul",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_consul.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.60",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 1,
}

## Server Nomad
server1_nomad_template_dict = {
    "template_name": "Server 1 Nomad",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_nomad.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.60",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 1,
    "retry_join_ips": retry_join_ips,
}

## Server Nomad
server2_nomad_template_dict = {
    "template_name": "Server 2 Nomad",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_nomad.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.61",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 3,
    "retry_join_ips": retry_join_ips,
}

## Server Nomad
server3_nomad_template_dict = {
    "template_name": "Server 3 Nomad",
    "template_file": f"{hashi_server_templates_dir}/hashi-up-server_nomad.j2",
    "template_type": "server",
    "cluster_server_ip": "192.168.1.62",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "bootstrap_expect": 3,
    "retry_join_ips": retry_join_ips,
}

## Agent 1 Consul
agent1_consul_template_dict = {
    "template_name": "Agent 1 Consul",
    "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_consul.j2",
    "template_type": "agent",
    "cluster_server_ip": "192.168.1.60",
    "cluster_agent_ip": "192.168.1.61",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "retry_join_ips": retry_join_ips,
}

## Agent 1 Nomad
agent1_nomad_template_dict = {
    "template_name": "Agent 1 Nomad",
    "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_nomad.j2",
    "template_type": "agent",
    "cluster_server_ip": "192.168.1.60",
    "cluster_agent_ip": "192.168.1.61",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "retry_join_ips": retry_join_ips,
}

## Agent 2 Consul
agent2_consul_template_dict = {
    "template_name": "Agent 2 Consul",
    "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_consul.j2",
    "template_type": "agent",
    "cluster_server_ip": "192.168.1.60",
    "cluster_agent_ip": "192.168.1.62",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "retry_join_ips": retry_join_ips,
}

## Agent 2 Nomad
agent2_nomad_template_dict = {
    "template_name": "Agent 2 Nomad",
    "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_nomad.j2",
    "template_type": "agent",
    "cluster_server_ip": "192.168.1.60",
    "cluster_agent_ip": "192.168.1.62",
    "ssh_target_user": "ubuntu",
    # "ssh_target_key": hashi_cluster_privkey,
    "ssh_target_key": host_privkey,
    "outfile_ext": ".sh",
    "connect_enabled": True,
    "retry_join_ips": retry_join_ips,
}

default_template_dict_list: list[dict[str, dict]] = [
    server1_consul_template_dict,
    # server2_consul_template_dict,
    # server3_consul_template_dict,
    server1_nomad_template_dict,
    # server2_nomad_template_dict,
    # server3_nomad_template_dict,
    agent1_consul_template_dict,
    agent1_nomad_template_dict,
    agent2_consul_template_dict,
    agent2_nomad_template_dict,
]
