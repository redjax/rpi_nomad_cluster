from dataclasses import dataclass, field
from jinja2 import FileSystemLoader, Environment
from pathlib import Path
from typing import Union
import os
from constants import valid_template_types


@dataclass
class HashiTemplateBase:
    template_name: str = field(default=None)
    template_file: str = field(default=None)
    template_type: str = field(default=None)
    outfile_ext: str = field(default=".hcl")

    @property
    def script_name(self) -> str:
        _start = self.template_name

        _script_name = _start.replace(" ", "-").lower() + self.outfile_ext

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
class NomadJobTemplateBase(HashiTemplateBase):
    dc_name: str = field(default="dc1")
    server_ip: str = field(default=None)
    service_name: str = field(default=None)
    docker_img: str = field(default=None)
