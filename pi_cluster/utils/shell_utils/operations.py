from __future__ import annotations

import os

from pathlib import Path
import subprocess
from typing import Optional, Union

from constants import scripts_export_dir
from loguru import logger as log

def execute_rendered_script(script_path: Path = None) -> bool:
    """Execute script at script_path.

    Return True (for success) or False (for failure).
    """
    try:
        _stdout = subprocess.check_output(
            script_path.__str__(), shell=True, stderr=subprocess.STDOUT, text=True
        )
        log.info(f"Script output:\n{_stdout}")

        return True
    except subprocess.CalledProcessError as exc:
        log.error(
            f"Script execution failed. Exit code: {exc.returncode}\nOutput:{exc.output}"
        )

        return False


def execute_all_rendered_scripts(script_dir: Union[Path, str] = scripts_export_dir):
    if not script_dir:
        raise ValueError("Missing directory to search for scripts in")
    if not isinstance(script_dir, Path):
        if isinstance(script_dir, str):
            script_dir: Path = Path(script_dir)
        else:
            raise TypeError(
                f"Invalid type for script_dir: ({type(script_dir)}). Must be one of [Path, str]"
            )

    if not script_dir.exists():
        raise FileNotFoundError(f"Could not find script path: {script_dir}")

    for _script in script_dir.iterdir():
        if not _script.is_file():
            pass

        if not _script.suffix == ".sh":
            raise ValueError(
                f"Invalid filetype: {_script.suffix}. Must be a .sh script"
            )

        script_path: Path = Path(f"{scripts_export_dir.__str__()}/{_script.name}")
        log.debug(f"Script path: {script_path}")

        log.debug(f"Executing script: {script_path}")

        res = execute_rendered_script(script_path=script_path)
        log.debug(f"Script {_script.name} execution results: {res}")
