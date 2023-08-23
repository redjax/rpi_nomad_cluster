from __future__ import annotations

from dataclasses import dataclass, field
import os

from pathlib import Path
from typing import Optional, Union

from jinja2 import Environment, FileSystemLoader

valid_template_types: list[str] = ["server", "agent"]


@dataclass
class HashiTemplateBase:
    template_name: str = field(default=None)
    template_file: str = field(default=None)
    template_type: str = field(default=None)
    cluster_server_ip: str = field(default=None)
    ## Only needed if target is a cluster Agent
    cluster_agent_ip: Optional[str] = field(default=None)
    ssh_target_user: Optional[str] = field(default="ubuntu")
    ssh_target_key: Optional[str] = field(default=None)

    @property
    def script_name(self) -> str:
        _start = self.template_name

        _script_name = _start.replace(" ", "-").lower() + ".sh"

        return _script_name

    @property
    def template(self):
        # raise NotImplementedError("Loading template file not yet implemented")

        try:
            templ_dir: Path = Path(self.template_file).parent
            loader = FileSystemLoader(searchpath=templ_dir)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception getting FileSystemLoader. Details: {exc}"
            )

        try:
            loader_env = Environment(loader=loader)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception getting Loader Environment. Details: {exc}"
            )

        try:
            templ_file: Path = Path(self.template_file).name
            _template = loader_env.get_template(templ_file)

            return _template
        except Exception as exc:
            raise Exception(f"Unhandled exception loading template. Details: {exc}")

    def render_template(self):
        # raise NotImplementedError("Rendering template to file not yet implemented")

        render_output = self.template.render(self.__dict__)

        return render_output

    def to_file(self, output_dir: Union[str, Path] = None):
        if output_dir is None:
            raise ValueError("Missing output_dir")

        if not isinstance(output_dir, Path):
            if isinstance(output_dir, str):
                output_dir = Path(output_dir)

            else:
                raise TypeError(
                    f"Invalid type for output_dir: {type(output_dir)}. Must be one of [str, Path]"
                )

        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)

        render = self.render_template()

        output_path: Path = Path(f"{output_dir}/{self.script_name}")

        try:
            with open(output_path, "w") as _out:
                _out.write(render)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception rendering template to file: {output_path}. Details: {exc}"
            )

        try:
            os.chmod(output_path, 0o755)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception setting chmod 755 on {output_path}. Details: {exc}"
            )

    def __post_init__(self):
        if self.template_type not in valid_template_types:
            raise ValueError(
                f"Invalid template_type: {self.template_type}. Must be one of {valid_template_types}"
            )


@dataclass
class HashiTemplate(HashiTemplateBase):
    pass


@dataclass
class HashiServerTemplate(HashiTemplateBase):
    pass


@dataclass
class HashiAgentTemplate(HashiTemplateBase):
    pass


@dataclass
class HashiTemplatesList:
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
