from __future__ import annotations

from dataclasses import dataclass, field
import os

from pathlib import Path
import shutil
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


@dataclass
class SSHKeyPair:
    private_key: SSHKeyHandler = field(default=None)
    public_key: SSHKeyHandler = field(default=None)

    @property
    def key_list(self) -> list[SSHKeyHandler]:
        keys = [self.private_key, self.public_key]

        return keys

    @property
    def as_dict(self) -> dict[str, SSHKeyHandler]:
        self_dict = {"private": self.private_key, "public": self.public_key}

        return self_dict

    def copy_keys(self) -> dict[str, bool]:
        privkey_input_path: Path = self.private_key.input_key_path
        privkey_output_path: Path = self.private_key.output_path

        pubkey_input_path: Path = self.public_key.input_key_path
        pubkey_output_path: Path = self.public_key.output_path

        def copy_self_key(
            input_key_path: Path = None, output_path: Path = None
        ) -> bool:
            if not input_key_path.exists():
                raise FileNotFoundError(f"Key not found at {input_key_path}")

            if not output_path.exists():
                log.debug(
                    f"Key not found at destination: {output_path.__str__()}. Copying key from [{input_key_path.__str__()}] -> [{output_path.__str__()}]"
                )

                ## Key not found at output_path, try copying
                try:
                    shutil.copy(src=input_key_path, dst=output_path)

                    return True
                except Exception as exc:
                    log.error(
                        Exception(
                            f"Unhandled exception copying private key from {input_key_path.__str__()} to {output_path.__str__()}. Details: {exc}"
                        )
                    )
                    return False

            else:
                ## Key was found at output_path
                log.debug(f"Key already exists: {output_path.__str__()}")
                return True

        privkey_copy = copy_self_key(
            input_key_path=privkey_input_path, output_path=privkey_output_path
        )
        pubkey_copy = copy_self_key(
            input_key_path=pubkey_input_path, output_path=pubkey_output_path
        )

        results = {"private_key": privkey_copy, "public_key": pubkey_copy}

        return results
