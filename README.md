Libvirt Inventory
=================
I wasn't happy with what was provided for libvirt in contrib for Ansible, so I tried to make it as python as possible.  I didn't look around too hard and realized it probably should be a plugin, but I don't have time for that.  This works now, maybe I'll get around to fixing it, or maybe you will?

The point of this script is to report back all hosts that libvirt is aware of and group them by active or inactive and report what host those systems are on.  I tried to follow guidelines on what is reported back.  It looks pretty, but it still needs testing to see if Ansible likes the output.

My hope is to use this with libvirt-nss as a way of managing multiple guests on multiple systems using libvirt-nss to help me figure out how to get to them from another system.