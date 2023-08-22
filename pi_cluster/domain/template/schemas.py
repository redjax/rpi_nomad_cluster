from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from jinja2 import Environment, FileSystemLoader


valid_template_types: list[str] = ["server", "agent"]


@dataclass
class HashiTemplatesList:
    servers: list[Path] = field(default=None)
    agents: list[Path] = field(default=None)

    @property
    def count_servers(self) -> int:
        return len(self.servers)

    @property
    def count_agents(self) -> int:
        return len(self.agents)


@dataclass
class HashiTemplateBase:
    template_file: str = field(default=None)
    template_type: str = field(default=None)
    cluster_server_ip: str = field(default=None)
    ## Only needed if target is a cluster Agent
    cluster_agent_ip: Optional[str] = field(default=None)
    ssh_target_user: Optional[str] = field(default="ubuntu")
    ssh_target_key: Optional[str] = field(default=None)

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
