from dataclasses import dataclass, field
from typing import Optional
from ..base_schemas import HashiTemplateBase, NomadJobTemplateBase


@dataclass
class NomadJobTemplate(NomadJobTemplateBase):
    pass


@dataclass
class NomadJobTraefik(NomadJobTemplateBase):
    http_port: Optional[int] = field(default=80)
    admin_port: Optional[int] = field(default=8080)
    api_dashboard: str = field(default="true")
    api_insecure: str = field(default="true")


@dataclass
class NomadJobNextcloud(NomadJobTemplateBase):
    http_port: Optional[int] = field(default=80)
    https_port: Optional[int] = field(default=443)
    resource_memory: Optional[int] = field(default=2048)
