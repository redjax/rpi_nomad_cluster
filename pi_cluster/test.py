import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path
from typing import Union

from domain.ssh import SSHKeyHandler, SSHKeyPair

from red_utils.loguru_utils import init_logger
from loguru import logger as log


init_logger()

templates_dir: str = "templates"
hashi_up_templates_dir: str = f"{templates_dir}/hashi-up"
hashi_server_templates_dir: str = f"{hashi_up_templates_dir}/server"
hashi_agent_templates_dir: str = f"{hashi_up_templates_dir}/agent"


if __name__ == "__main__":
    hashi_cluster_privkey: str = (
        "../ansible/roles/security/hashi-ssh-setup/files/hashi-pi_id_rsa"
    )
    hashi_cluster_pubkey: str = (
        "../ansible/roles/security/hashi-ssh-setup/files/hashi-pi_id_rsa.pub"
    )

    private_key = SSHKeyHandler(input_key_path=hashi_cluster_privkey)
    public_key = SSHKeyHandler(input_key_path=hashi_cluster_pubkey)

    _keys: SSHKeyPair = SSHKeyPair(private_key=private_key, public_key=public_key)
    log.debug(f"Keys: {_keys}")

    log.info("Copying keys")
    copy_keys = _keys.copy_keys()
    log.debug(f"Results: {copy_keys}")

    """

    ## Server Consul
    server_consul_template_dict = {
        "template_file": f"{hashi_server_templates_dir}/hashi-up-server_consul.j2",
        "template_type": "server",
        "cluster_server_ip": "192.168.1.60",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    server_consul_template: HashiTemplate = HashiTemplate(**server_consul_template_dict)
    log.debug(f"Server Consul template: {server_consul_template}")
    log.debug(f"Test load server Consul template: {server_consul_template.template}")
    ## End server Consul

    ## Server Nomad
    server_nomad_template_dict = {
        "template_file": f"{hashi_server_templates_dir}/hashi-up-server_nomad.j2",
        "template_type": "server",
        "cluster_server_ip": "192.168.1.60",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    server_nomad_template: HashiTemplate = HashiTemplate(**server_nomad_template_dict)
    log.debug(f"Server Nomad template: {server_nomad_template}")
    log.debug(f"Test load server Nomad template: {server_nomad_template.template}")
    ## End server Nomad

    ## Agent 1 Consul
    agent1_consul_template_dict = {
        "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_consul.j2",
        "template_type": "agent",
        "cluster_server_ip": "192.168.1.60",
        "cluster_agent_ip": "192.168.1.61",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    agent1_consul_template: HashiTemplate = HashiTemplate(**agent1_consul_template_dict)
    log.debug(f"Agent Consul template: {agent1_consul_template}")
    log.debug(f"Test load agent Consul template: {agent1_consul_template.template}")
    ## End agent 1 Consul

    ## Agent 1 Nomad
    agent1_nomad_template_dict = {
        "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_nomad.j2",
        "template_type": "agent",
        "cluster_server_ip": "192.168.1.60",
        "cluster_agent_ip": "192.168.1.61",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    agent1_nomad_template: HashiTemplate = HashiTemplate(**agent1_nomad_template_dict)
    log.debug(f"Agent Nomad template: {agent1_nomad_template}")
    log.debug(f"Test load agent Nomad template: {agent1_nomad_template.template}")
    ## End agent 1 Nomad

    ## Agent 1 Consul
    agent1_consul_template_dict = {
        "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_consul.j2",
        "template_type": "agent",
        "cluster_server_ip": "192.168.1.60",
        "cluster_agent_ip": "192.168.1.61",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    agent1_consul_template: HashiTemplate = HashiTemplate(**agent1_consul_template_dict)
    log.debug(f"Agent 1 Consul template: {agent1_consul_template}")
    log.debug(f"Test load agent 1 Consul template: {agent1_consul_template.template}")
    ## End agent 1 Consul

    ## Agent 2 Nomad
    agent2_nomad_template_dict = {
        "template_file": f"{hashi_agent_templates_dir}/hashi-up-agent_nomad.j2",
        "template_type": "agent",
        "cluster_server_ip": "192.168.1.60",
        "cluster_agent_ip": "192.168.1.62",
        "ssh_target_user": "ubuntu",
        "ssh_target_key": hashi_cluster_privkey,
    }
    agent2_nomad_template: HashiTemplate = HashiTemplate(**agent2_nomad_template_dict)
    log.debug(f"Agent Nomad 2 template: {agent2_nomad_template}")
    log.debug(f"Test load agent 2 Nomad template: {agent2_nomad_template.template}")
    ## End agent 1 Nomad

    ## Render server 1 Consul
    log.info("Test render Server Consul template")
    render_server_consul = server_consul_template.render_template()
    log.debug(f"Render server Consul template output:\n{render_server_consul}")
    ## End render server 1 Consul

    ## Render server 1 Consul
    log.info("Test render Server Nomad template")
    render_server_nomad = server_nomad_template.render_template()
    log.debug(f"Render server Nomad template output:\n{render_server_nomad}")
    ## End render server 1 Consul

    """
