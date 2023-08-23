from __future__ import annotations

from constants import (
    default_template_dict_list,
    hashi_cluster_privkey,
    hashi_cluster_pubkey,
    host_privkey,
    host_pubkey,
)
from domain.ssh import SSHKeyHandler, SSHKeyPair
from domain.template import HashiTemplate, HashiTemplatesList
from loguru import logger as log

def get_ssh_keys(
    # private_key_path: str = hashi_cluster_privkey,
    # public_key_path: str = hashi_cluster_pubkey,
    private_key_path: str = host_privkey,
    public_key_path: str = host_pubkey,
) -> SSHKeyPair:
    private_key = SSHKeyHandler(input_key_path=private_key_path)
    public_key = SSHKeyHandler(input_key_path=public_key_path)

    _keys: SSHKeyPair = SSHKeyPair(private_key=private_key, public_key=public_key)

    return _keys


def get_server_agent_templates(
    template_dicts: list[dict[str, str]] = default_template_dict_list
) -> HashiTemplatesList:
    """Return a list of HashiTemplate class objects.

    Uses default dicts defined in constants.py. Override by passing a new
    list of template dict objects for template_dicts.
    """
    servers: list[HashiTemplate] = []
    agents: list[HashiTemplate] = []

    for in_templ in template_dicts:
        # log.debug(f"Template dict ({type(in_templ)}): {in_templ}")
        template_obj: HashiTemplate = HashiTemplate(**in_templ)
        # log.debug(f"Template class ({type(template_obj)}): {template_obj}")

        match template_obj.template_type:
            case "server":
                servers.append(template_obj)
            case "agent":
                servers.append(template_obj)
            case _:
                log.error(
                    f"Invalid template type: {template_obj.template_type}. Must be 'server' or 'agent'"
                )

    _templates = HashiTemplatesList(servers=servers, agents=agents)

    return _templates
