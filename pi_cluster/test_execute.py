from loguru import logger as log
from pathlib import Path
from typing import Union, Optional

from constants import (
    scripts_export_dir,
    host_privkey,
    default_template_dict_list,
    scripts_export_dir,
)
from dependencies import get_server_agent_templates, get_ssh_keys

import paramiko

if __name__ == "__main__":
    _keys = get_ssh_keys()
    templates = get_server_agent_templates()
    server_templates = templates.servers
    agent_templates = templates.agents

    scripts: list[Path] = []

    for _script in scripts_export_dir.iterdir():
        if _script.is_file():
            if _script.suffix == ".sh":
                scripts.append(_script)

    log.debug(f"Scripts ({len(scripts)}): {scripts}")

    ssh_client: paramiko.SSHClient = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_pkey: paramiko.RSAKey = paramiko.RSAKey(filename=host_privkey)

    test_server = server_templates[0]

    ssh_client.connect(
        test_server.cluster_server_ip,
        username=test_server.ssh_target_user,
        pkey=ssh_pkey,
    )

    try:
        with ssh_client as c:
            stdin, stdout, stderr = c.exec_command("ls")

        log.debug(f"Command output:\n{stdout.read().decode()}")
    except Exception as exc:
        raise Exception(
            f"Unhandled exception connecting to host {test_server.cluster_server_ip}. Details: {exc}"
        )
