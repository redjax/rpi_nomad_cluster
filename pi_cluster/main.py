import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path
from typing import Union

from domain.template import (
    HashiAgentTemplate,
    HashiServerTemplate,
    HashiTemplate,
    HashiTemplatesList,
)
from domain.ssh import SSHKeyHandler, SSHKeyPair

from red_utils.loguru_utils import init_logger
from loguru import logger as log

from constants import (
    export_dir,
    templates_dir,
    hashi_up_templates_dir,
    hashi_server_templates_dir,
    hashi_agent_templates_dir,
    hashi_cluster_privkey,
    hashi_cluster_pubkey,
    server_consul_template_dict,
    server_nomad_template_dict,
    agent1_consul_template_dict,
    agent2_consul_template_dict,
    agent1_nomad_template_dict,
    agent2_nomad_template_dict,
)
from dependencies import get_ssh_keys


init_logger()


def get_server_agent_templates() -> HashiTemplatesList:
    server_consul_template: HashiTemplate = HashiTemplate(**server_consul_template_dict)
    server_nomad_template: HashiTemplate = HashiTemplate(**server_nomad_template_dict)
    agent1_nomad_template: HashiTemplate = HashiTemplate(**agent1_nomad_template_dict)
    agent1_consul_template: HashiTemplate = HashiTemplate(**agent1_consul_template_dict)
    agent2_consul_template: HashiTemplate = HashiTemplate(**agent2_consul_template_dict)
    agent2_nomad_template: HashiTemplate = HashiTemplate(**agent2_nomad_template_dict)

    servers = [server_consul_template, server_nomad_template]
    agents = [
        agent1_consul_template,
        agent1_nomad_template,
        agent2_consul_template,
        agent2_nomad_template,
    ]

    _templates = HashiTemplatesList(servers=servers, agents=agents)

    return _templates


def demo_run(DEBUG: bool = False):
    ## Copy SSH keys to filesystem
    log.info("Copying keys")
    _keys = get_ssh_keys()
    log.debug(f"Keys: {_keys}")

    copy_keys = _keys.copy_keys()
    log.debug(f"Results: {copy_keys}")

    all_templates = get_server_agent_templates()

    if DEBUG:
        for _srv in all_templates.servers:
            render = _srv.render_template()
            log.debug(f"[{_srv.script_name}] {_srv.template_name} render:\n{render}")

            _srv.to_file()

        for _ag in all_templates.agents:
            render = _ag.render_template()
            log.debug(f"[{_ag.script_name}] {_ag.template_name} render:\n{render}")

            _ag.to_file()

    ## Render to file
    for _srv in all_templates.servers:
        log.debug(f"Rendering {_srv.script_name} to file")

        _srv.to_file(output_dir="export/script")

    for _ag in all_templates.agents:
        log.debug(f"Rendering {_ag.script_name} to file")

        _ag.to_file(output_dir="export/script")


if __name__ == "__main__":
    demo_run(DEBUG=False)
