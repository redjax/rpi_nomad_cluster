from __future__ import annotations

from dataclasses import dataclass, field
import os

from pathlib import Path
from typing import Optional, Union

from jinja2 import Environment, FileSystemLoader

from constants import valid_template_types

from .base_schemas import HashiTemplateBase


@dataclass
class HashiTemplate(HashiTemplateBase):
    pass


@dataclass
class HashiServerTemplate(HashiTemplateBase):
    cluster_server_ip: str = field(default=None)
    ssh_target_user: Optional[str] = field(default="ubuntu")
    ssh_target_key: Optional[str] = field(default=None)
    bootstrap_expect: int = field(default=1)


@dataclass
class HashiAgentTemplate(HashiTemplateBase):
    cluster_agent_ip: Optional[str] = field(default=None)
    cluster_server_ip: str = field(default=None)
    ssh_target_user: Optional[str] = field(default="ubuntu")
    ssh_target_key: Optional[str] = field(default=None)


@dataclass
class HashiClusterTemplatesList:
    servers: list[HashiTemplate] = field(default=None)
    agents: list[HashiTemplate] = field(default=None)

    @property
    def count_servers(self) -> int:
        return len(self.servers)

    @property
    def count_agents(self) -> int:
        return len(self.agents)

    @property
    def all(self) -> list[HashiTemplate]:
        _all = []

        for _srv in self.servers:
            _all.append(_srv)

        for _ag in self.agents:
            _all.append(_ag)

        return _all

    def render_all(self, template_type: str = "both"):
        valid_template_types: list[str] = ["servers", "agents", "both"]

        if not template_type:
            raise ValueError("Missing input_type")
        if template_type not in valid_template_types:
            raise ValueError(
                f"Invalid template_type: {template_type}. Must be one of {valid_template_types}"
            )

        match template_type:
            case "both":
                for _ag_srv in self.servers:
                    _render = _ag_srv.render_template()
                    print(f"Render:\n{_render}")

                for _ag_templ in self.agents:
                    _render = _ag_templ.render_template()
                    print(f"Render:\n{_render}")
            case "servers":
                for _ag_srv in self.servers:
                    _render = _ag_srv.render_template()
                    print(f"Render:\n{_render}")
            case "agents":
                for _ag_templ in self.agents:
                    _render = _ag_templ.render_template()
                    print(f"Render:\n{_render}")
