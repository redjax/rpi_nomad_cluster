# Raspberry Pi - Nomad Cluster

Utilize [`hashi-up`](https://github.com/jsiebens/hashi-up) to create a [`nomad`](https://www.nomadproject.io)/[`consul`](https://www.consul.io) (with optional [`vault`](https://www.vaultproject.io)) cluster on 3+ Raspberry Pis.

## The Stack

- 3 Raspberry Pi 4B 8GB
  - server
	- Hostname: rpi-cl-srv1
	- OS: Raspbian Lite x64
  - agent 1
  	- Hostname: rpi-cl-ag1
  	- OS: Raspbian Lite x64 
  - agent 2
  	- Hostname: rpi-cl-ag2
  	- OS: Raspbian Lite x64

## Notes

### Setup instructions

- Requirements:
  - [`hashi-up`](https://github.com/jsiebens/hashi-up)
  - SSH credentials
    - On the server, generate a key with `ssh-keygen`, i.e. `$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/rpi_cl_id_rsa`
    - For some reason, even when the key is added to the remote during the `cloud-init` phase, I've found I still need to copy the ID with `ssh-copy-id -i ~/.ssh/<cluster_ssh_key> <user>@<rpi-host>` for each new server/agent

#### >Raspberry Pi Setup

- Choose 3 microSD cards of the same capacity & speed
- Use the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to write the `Ubuntu Server <major_ver>.<minor_ver> x64` image to each SD card
  - As of writing this guide, I used the `Ubuntu Server 23.04 (64-bit)` image under `Other general-purpose OS > Ubuntu` category
- Create/copy the `cloud-init` files (`cmdline.txt`, `meta-data`, `network-config`, `user-data`)
  - Examples of these files can be found in the [`pi_cluser/reference_files`](./pi_cluster/reference_files/) directory
  - Make sure to edit the following in each file:
    - `cmdline.txt`
      - No edits
    - `meta-data`
      - `instance_id`: Set to the chosen hostname for the Pi host
    - `network-config`
      - `addresses`: Set an address in the line that starts with `addresses`
        - Example:
        ```
        ...

        eth0:
          ...
          addresses:
            - 192.168.1.50
        ```
    - `user-data`
      - `hostname`
        - Set to the chosen hostname for the Pi host
      - `fqdn`
        - Set the Pi's FQDN, i.e. `hostname.domain`
      - `users > ssh_authorized_keys`: Set the `ssh-rsa` key(s) to copy/create on setup
        - Beforehand, create an SSH key to share for management of the Pi cluster
          - The private key (i.e. `id_rsa`) should exist on every server/computer that will connect to the cluster. **DO NOT COPY THE PRIVATE KEY TO THE PIs!!!**
          - The public key (i.e. `id_rsa.pub`) should be copied to each Pi in the cluster
          - You can `cat id_rsa.pub` and copy the output to `ssh_authorized_keys` in the `users` section
      - `netplan` (section begins with `- path: /etc/netplan/custom-cloud-init.yaml`)
        - In the `content` section, look for a line that starts with `addresses:`
          - Edit the address, i.e. `192.168.1.50/24`
- Once `cloud-init` is complete on the Pis, if you can't log in via SSH, manually copy the public key to each host
  - `ssh-copy-id -i /path/to/public_key.pub <pi-user>@<pi-ip/pi-hostname>`
  - For easy SSH by hostname (i.e. `ssh rpi-cluster-host1`), add a line to your `~/.ssh/config` for each host:
    ```
    Host rpi-cluster-host1
      HostName 192.168.1.xxx
      User <pi-user>
      IdentityFile ~/.ssh/private_key
    ```

#### >Ansible Setup

## Links

- [Cloud-init docs](https://cloudinit.readthedocs.io/en/latest/)
- [Cloud-init reference](https://cloudinit.readthedocs.io/en/latest/reference/index.html)
- [Hashi-Up's creator demo of a nomad cluster](https://johansiebens.dev/posts/2020/08/building-a-nomad-cluster-on-raspberry-pi-running-ubuntu-server/)
- [Running Hashicorp Nomad, Consul, Pihole and Gitea on Raspberry Pi 3 B+](https://medium.com/swlh/running-hashicorp-nomad-consul-pihole-and-gitea-on-raspberry-pi-3-b-f3f0d66c907)
- [Github: Ubuntu 20.04+ WiFi & cloud-init RPi4B](https://github.com/martadinata666/cloud-init)
- [Jorge Sancho Personal Blog: Raspberry cluster up and running](https://jslarraz.es/blog_page.html?_id=2022-10-25)
- [Github: mjpitz/rpi-clout-init reference repo](https://github.com/mjpitz/rpi-cloud-init/tree/main)
- [Github: timebertt/pi-cloud-init reference repo](https://github.com/timebertt/pi-cloud-init/tree/master)
