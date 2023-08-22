from dataclasses import dataclass, field
import os
import shutil
from pathlib import Path
from typing import Union

from loguru import logger as log


@dataclass
class SSHKeyHandler:
    input_key_path: Union[Path, str] = None

    @property
    def output_path(self) -> Path:
        output: Path = Path(f"/home/{os.getlogin()}/.ssh/{self.input_key_path.name}")

        return output

    def copy_key(self) -> bool:
        if not self.input_key_path.exists():
            raise FileNotFoundError(f"Key not found at {self.input_key_path}")

        if not self.output_path.exists():
            log.debug(
                f"Key not found at destination: {self.output_path.__str__()}. Copying key from [{self.input_key_path.__str__()}] -> [{self.output_path.__str__()}]"
            )

            ## Key not found at output_path, try copying
            try:
                shutil.copy(src=self.input_key_path, dst=self.output_path)

                return True
            except Exception as exc:
                log.error(
                    Exception(
                        f"Unhandled exception copying private key from {self.input_key_path.__str__()} to {self.output_path.__str__()}. Details: {exc}"
                    )
                )
                return False

        else:
            ## Key was found at output_path
            log.info(f"Key already exists: {self.output_path.__str__()}")
            return True

    def __post_init__(self):
        if not isinstance(self.input_key_path, Path):
            if isinstance(self.input_key_path, str):
                self.input_key_path = Path(self.input_key_path)
            else:
                raise ValueError(
                    f"Invalid type for input_key_path: {type(self.input_key_path)}. Must be of type str"
                )

        return self
