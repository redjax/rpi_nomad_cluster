from constants import (
    hashi_cluster_pubkey,
    hashi_cluster_privkey,
    host_privkey,
    host_pubkey,
)
from domain.ssh import SSHKeyHandler, SSHKeyPair


def get_ssh_keys(
    # private_key_path: str = hashi_cluster_privkey,
    # public_key_path: str = hashi_cluster_pubkey,
    private_key_path: str = host_privkey,
    public_key_path: str = host_pubkey,
) -> SSHKeyPair:
    private_key = SSHKeyHandler(input_key_path=private_key_path)
    public_key = SSHKeyHandler(input_key_path=public_key_path)

    _keys: SSHKeyPair = SSHKeyPair(private_key=private_key, public_key=public_key)

    return _keys
