#!/usr/bin/env python

import sys
import libvirt
import json
import socket

# We want to gather the hostname for Ansible.
hostname = socket.gethostbyaddr(socket.gethostname())[0]
# We want this to run on the local system only.
host_domain = 'qemu:///system'

# Initialize the dictionary.  May be a horrible way to deal with it, but I am too new to it to make it better.
inventory = {}
inventory['_meta'] = {}
inventory['_meta']['hostvars'] = {}
inventory['all'] = {}
inventory['all']['vars'] = {}
inventory['all']['vars']['ansible_host'] = hostname
inventory['all']['children'] = ['active', 'inactive', 'ungrouped']
inventory['active'] = {}
inventory['active']['vars'] = {}
inventory['active']['vars']['ansible_host'] = hostname
inventory['inactive'] = {}
inventory['inactive']['vars'] = {}
inventory['inactive']['vars']['ansible_host'] = hostname

virthost = libvirt.open(host_domain)
if virthost == None:
    sys.stderr.write('Failed to open connection to ' + host_domain, file=sys.stderr)
    exit(1)

# It took me a bit to figure out that there is no constant for all domains, just 0.  Hint was in libvirt-domain.h
alldomains = virthost.listAllDomains(0)
activedomains = virthost.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
inactivedomains = virthost.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE)

inventory['active']['hosts'] = [domain.name() for domain in activedomains]
inventory['inactive']['hosts'] = [domain.name() for domain in inactivedomains]

if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(inventory, indent=4, sort_keys=True))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    print(json.dumps({'ansible_connection': 'libvirt_lxc'}))
else:
    sys.stderr.write("Need an argument, either --list or --host <host>\n")

virthost.close()
exit()
