from __future__ import annotations

import stackprinter

stackprinter.set_excepthook(style="darkbg2")

from pathlib import Path
from typing import Union

from constants import (
    agent1_consul_template_dict,
    agent1_nomad_template_dict,
    agent2_consul_template_dict,
    agent2_nomad_template_dict,
    default_template_dict_list,
    export_dir,
    hashi_agent_templates_dir,
    hashi_cluster_privkey,
    hashi_cluster_pubkey,
    hashi_server_templates_dir,
    hashi_up_templates_dir,
    scripts_export_dir,
    server_consul_template_dict,
    server_nomad_template_dict,
    templates_dir,
)
from dependencies import get_server_agent_templates, get_ssh_keys
from domain.ssh import SSHKeyHandler, SSHKeyPair
from domain.template import (
    HashiAgentTemplate,
    HashiServerTemplate,
    HashiTemplate,
    HashiTemplatesList,
)
from loguru import logger as log
from red_utils.loguru_utils import init_logger
from utils.shell_utils import execute_all_rendered_scripts, execute_rendered_script

init_logger()


def default_setup(
    ssh_keys: SSHKeyPair = None, templates: HashiTemplatesList = None
) -> None:
    if not ssh_keys:
        raise ValueError("Missing SSHKeyPair object")
    if not isinstance(ssh_keys, SSHKeyPair):
        raise TypeError(
            f"Invalid type for ssh_keys: ({type(ssh_keys)}). Must be of type SSHKeyPair"
        )

    if not templates:
        raise ValueError("Missing templates list")
    if not isinstance(templates, HashiTemplatesList):
        raise TypeError(
            f"Invalid type for templates: ({type(templates)}). Must be of type HashiTemplatesList"
        )

    ## Copy SSH keys
    log.info("Copying SSH keys")
    copy_keys = _keys.copy_keys()
    log.info(f"Key copy success: {copy_keys}")

    log.info(f"Rendering templates to files in {scripts_export_dir}")
    ## Render templates to file
    for _srv in templates.servers:
        log.debug(f"Rendering {_srv.script_name} to file")

        _srv.to_file(output_dir=scripts_export_dir)

    for _ag in templates.agents:
        log.debug(f"Rendering {_ag.script_name} to file")

        _ag.to_file(output_dir=scripts_export_dir)


if __name__ == "__main__":
    log.info("App start")

    ## Load SSH keys
    _keys = get_ssh_keys()
    ## Load templates
    all_templates = get_server_agent_templates()

    ## Perform default setup
    default_setup(ssh_keys=_keys, templates=all_templates)

    log.info("Executing all rendered scripts")
    execute_all_rendered_scripts()
