from __future__ import annotations

from pathlib import Path
from typing import Optional

from domain.template import HashiClusterTemplatesList
from jinja2 import Environment, FileSystemLoader, Template
from loguru import logger as log


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
        raise Exception("Missing template_dir_path value")

    log.debug(f"Creating template loader for dir: [{template_dir_path}]")

    try:
        _loader = FileSystemLoader(searchpath=template_dir_path)
    except Exception as exc:
        raise Exception(
            f"Unhandled exception creating FileSystemLoader for template path: {template_dir_path}. Details: {exc}"
        )

    return _loader


def create_loader_env(_loader: FileSystemLoader = None) -> Environment:
    """Create a jinja2.Environment object for the Jinja template loader object passed
    as _loader.

    The environment is used to pass data and output a templated file.
    """
    if not _loader:
        raise ValueError("Missing _loader value")

    log.debug("Creating template environment for loader.")

    try:
        _env = Environment(loader=_loader)
    except Exception as exc:
        raise Exception(f"Unhandled exception creating loader env. Details: {exc}")

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


def load_hashi_up_templates(templates: list[Path] = []) -> HashiClusterTemplatesList:
    """Sort a list of Agent & Server templates into a HashiTemplates object."""
    templates_dict: dict[str, list[Path]] = {"servers": [], "agents": []}

    if not templates:
        raise ValueError("Missing list of templates")
    if not isinstance(templates, list):
        raise TypeError(
            f"Invalid type for templates: ({type(templates)}). Must be a list of Path objects"
        )
    for _t in templates:
        if not isinstance(_t, Path):
            raise TypeError(
                f"Invalid type for list object: ({type(_t)}). Must be of type Path"
            )

    for _templ in templates:
        if _templ.parent.name == "agent":
            templates_dict["agents"].append(_templ)
        elif _templ.parent.name == "server":
            templates_dict["servers"].append(_templ)
        else:
            log.warning(Exception(f"Unknown parent dir: {_templ.parent.name}"))
            pass

    try:
        templates: HashiClusterTemplatesList = HashiClusterTemplatesList(
            **templates_dict
        )
    except Exception as exc:
        raise Exception(
            f"Unhandled exception converting loaded templates dict to HashiTemplates class instance. Details: {exc}"
        )

    return templates
