# ansible-mitre
MITRE playbooks using ansible format

## Prerequisites
ansible (`apt-get install ansible`)

## Installation
- `git clone https://github.com/rallyspeed/Azure-CIS.git`

## Usage
- `ansible-playbook [playbook].yaml`

## Optional INSTALL SEPHAMORE GUI
INSTALL  sephamore for GUI interface.
 - `apt-get install mysql-server`
 - `mysql_secure_installation`
 - `wget https://github.com/ansible-semaphore/semaphore/releases/download/v2.5.1/semaphore_2.5.1_linux_amd64.deb`
 - `dpkg -i semaphore_2.5.1_linux_amd64.deb`
 - `semaphore -setup`
## Optional RUN SEPHAMORE GUI
 - `ssh-add ~/.ssh/id_rsa`
 - `ssh -T git@github.com` To confirm ansible machine can reach the github repo
 - `semaphore -config /opt/config.json &`
 
