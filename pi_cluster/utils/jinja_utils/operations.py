from __future__ import annotations

from typing import Optional, Union
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


def get_templates(
    template_dir: str = None, template_files: list[Path] = []
) -> list[Path]:
    if not template_dir:
        raise ValueError("Missing template_dir")

    if not isinstance(template_dir, str):
        raise TypeError(
            f"Expected str value for template_dir, got {type(template_dir)}"
        )

    if not Path(template_dir).exists():
        raise FileNotFoundError(f"Could not find template directory: {template_dir}")

    if not Path(template_dir).is_dir():
        raise TypeError(f"Path is not a directory: {template_dir}")

    for f in Path(template_dir).iterdir():
        if Path(f).is_file():
            if Path(f).suffix == ".j2":
                template_files.append(f)

        elif Path(f).is_dir:
            get_templates(str(f), template_files)

    return template_files


def load_template_dir(template_dir_path: str = None) -> FileSystemLoader:
    """Create a jinja2.FileSystemLoader object for the directory passed as
    template_dir_path.

    This loader is used by Jinja to open .j2 template files.
    """
    if not template_dir_path:
        # log.debug("template_dir_path value empty. Skipping.")
        print("t[DEBUG] emplate_dir_path value empty. Skipping.")
        pass

    # log.debug(f"Creating template loader for dir: [{template_dir_path}]")
    print(f"[DEBUG] Creating template loader for dir: [{template_dir_path}]")
    _loader = FileSystemLoader(searchpath=template_dir_path)

    return _loader


def create_loader_env(_loader: FileSystemLoader = None) -> Environment:
    """Create a jinja2.Environment object for the Jinja template loader object passed
    as _loader.

    The environment is used to pass data and output a templated file.
    """
    if not _loader:
        # log.debug(f"_loader value empty. Skipping.")
        print(f"[DEBUG] _loader value empty. Skipping.")

    # log.debug(f"Creating template environment for loader.")
    print(f"[DEBUG] Creating template environment for loader.")

    _env = Environment(loader=_loader)

    return _env


def get_template_from_env(
    templ_env: Environment = None, templ_file: str = None
) -> Template:
    # log.debug(f"Template file: {templ_file}")
    print(f"[DEBUG] Template file: {templ_file}")
    _template = templ_env.get_template(templ_file)

    return _template


def render_template_to_file(
    _render: Optional[str] = None,
    _outfile: str = None,
) -> None:
    # log.debug(f"Rendering to [{_outfile}]")
    print(f"[DEBUG] Rendering to [{_outfile}]")

    with open(_outfile, "w") as _out:
        _out.write(_render)
