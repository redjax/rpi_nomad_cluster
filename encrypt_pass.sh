#!/bin/bash

# read -s -p "Enter a password to encrypt: " PASS

# echo "Encrypted password: "
# echo $(openssl passwd -1 -stdin <<<$PASS)

if ! command -v mkpasswd &>/dev/null; then
    echo "mkpasswd is not installed. Installing."
    sudo apt install -y whois
fi

mkpasswd --method=SHA-512 --rounds=4096
