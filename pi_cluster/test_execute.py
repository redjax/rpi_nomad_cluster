"""Test executing scripts rendered from Jinja templates."""
import os
import subprocess
from loguru import logger as log
from typing import Union, Optional
from pathlib import Path

script_log_dir: Path = Path("logs/script_stdout")


if __name__ == "__main__":
    if not script_log_dir.exists():
        script_log_dir.mkdir(parents=True, exist_ok=True)

    scripts_dir: Path = Path("export/script")
    log.debug(f"Scripts dir: {scripts_dir}")

    for _script in scripts_dir.iterdir():
        if not _script.is_file():
            pass

        if not _script.suffix == ".sh":
            raise ValueError(
                f"Invalid filetype: {_script.suffix}. Must be a .sh script"
            )

        script_path: Path = Path(f"{scripts_dir.__str__()}/{_script.name}")
        log.debug(f"Script path: {script_path}")

        log.debug(f"Testing with script: {script_path}")

        try:
            _stdout = subprocess.check_output(
                script_path.__str__(), shell=True, stderr=subprocess.STDOUT, text=True
            )
            log.info(f"Script output:\n{_stdout}")
        except subprocess.CalledProcessError as exc:
            log.error(
                f"Script execution failed. Exit code: {exc.returncode}\nOutput:{exc.output}"
            )
