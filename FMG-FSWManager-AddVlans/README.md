# FortiManager - FortiSwitch Manager 
This script will loop through a csv of firewalls and a CSV of VLANs and add a per device mapping for every VLAN on every device within FSW Manager.

## Supported configuratation
Currently only the following items are supported for configuration, but this could easily be expanded as needed using the FortiManager API documentation on [FNDN](https://fndn.fortinet.net/).

* Mapped Device
* VLAN ID
* IP/Netmask
* DHCP Server
* DHCP Range