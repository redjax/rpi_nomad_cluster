from __future__ import annotations

import os

from pathlib import Path
import shutil
from typing import Union

from loguru import logger as log

def get_logged_in_user() -> str:
    user = os.getlogin()

    return user


def copy_ssh_key(
    input_path: Union[str, Path] = None, output_path: Union[str, Path] = None
) -> bool:
    """Handle copying SSH private key from input_path to output_path."""
    if not input_path:
        raise ValueError("Missing an input path for key to copy")
    if not output_path:
        raise ValueError("Missing an output path to copy key to")

    if not isinstance(input_path, str) and not isinstance(input_path, Path):
        raise TypeError(
            f"Invalid type for input_path: {type(input_path)}. Must be one of [str, Path]"
        )
    if not isinstance(output_path, str) and not isinstance(output_path, Path):
        raise TypeError(
            f"Invalid type for output_path: {type(output_path)}. Must be one of [str, Path]"
        )

    ## Convert valid inputs to Path value, if they are not already Path objects
    if not isinstance(input_path, Path):
        input_path: Path = Path(input_path)
    if not isinstance(output_path, Path):
        output_path: Path = Path(output_path)

    ## Check for existence of input file before copying
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found at path: {input_path}")

    ## Check for existence of output file before copying
    if not output_path.exists():
        log.debug(
            f"Key not found at destination: {output_path.__str__()}. Copying key from [{input_path.__str__()}] -> [{output_path.__str__()}]"
        )

        ## Key not found at output_path, try copying
        try:
            shutil.copy(src=input_path, dst=output_path)

            return True
        except Exception as exc:
            log.error(
                Exception(
                    f"Unhandled exception copying private key from {input_path.__str__()} to {output_path.__str__()}. Details: {exc}"
                )
            )
            return False

    else:
        ## Key was found at output_path
        log.info(f"Key already exists: {output_path.__str__()}")
        return True
