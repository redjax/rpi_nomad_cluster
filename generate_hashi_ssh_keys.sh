#!/bin/bash

ansible_dir="ansible"
roles_dir="$ansible_dir/roles"
security_roles_dir="$roles_dir/security"
hashi_ssh_role_dir="$security_roles_dir/hashi-ssh-setup"
hashi_ssh_role_file_dir="$hashi_ssh_role_dir/files"

priv_keyname="hashi-pi_id_rsa"
public_keyname="hashi-pi_id_rsa"
key_encrypt="rsa"
key_bytes="4096"

if [[ ! -f "$hashi_ssh_role_file_dir/$priv_keyname" ]]; then
    echo "Creating SSH key pair at $hashi_ssh_role_file_dir"
    echo ""
    ssh-keygen -t $key_encrypt -b $key_bytes -f $hashi_ssh_role_file_dir/hashi-pi_id_rsa -N ""
else
    echo "SSH key pair already exists at $hashi_ssh_role_file_dir/$priv_keyname. Skipping key creation."
fi
