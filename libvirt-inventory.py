#!/usr/bin/env python

import sys
import libvirt
import json
import socket

hostname = socket.gethostbyaddr(socket.gethostname())[0]
host_domain = 'qemu:///system'

inventory = {}
inventory['_meta'] = {}
inventory['_meta']['hostvars'] = {}
inventory['all'] = {}
inventory['all']['vars'] = 'ansible_host=' + hostname
inventory['all']['children'] = {}
inventory['all']['children']['ungrouped'] = {}
inventory['active'] = {}
inventory['active']['vars'] = 'ansible_host=' + hostname
inventory['inactive'] = {}
inventory['inactive']['vars'] = 'ansible_host=' + hostname
inventory['ungrouped'] = {}

conn = libvirt.open(host_domain)
if conn == None:
    sys.stderr('Failed to open connection to ' + host_domain, file=sys.stderr)
    exit(1)

alldomains = conn.listAllDomains(0)
activedomains = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_ACTIVE)
inactivedomains = conn.listAllDomains(libvirt.VIR_CONNECT_LIST_DOMAINS_INACTIVE)

inventory['all']['hosts'] = [x.name() for x in alldomains]
inventory['active']['hosts'] = [x.name() for x in activedomains]
inventory['inactive']['hosts'] = [x.name() for x in inactivedomains]

if len(sys.argv) == 2 and sys.argv[1] == '--list':
    print(json.dumps(inventory, indent=4, sort_keys=True))
elif len(sys.argv) == 3 and sys.argv[1] == '--host':
    print(json.dumps({'ansible_connection': 'libvirt_lxc'}))
else:
    sys.stderr.write("Need an argument, either --list or --host <host>\n")

conn.close()
exit(0)