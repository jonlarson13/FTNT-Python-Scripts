# FortiManager - FortiSwitch Manager 
This script will loop through a CSV of firewalls and a CSV of VLANs and add a per device mapping for every VLAN on every device within FSW Manager.

## Supported configuration
Currently only the following items are supported for configuration, but this could easily be expanded as needed using the FortiManager API documentation on [FNDN](https://fndn.fortinet.net/).

* Mapped Device
* VLAN ID
* IP/Netmask
* DHCP Server
* DHCP Range

## Requirements
This script requires python3 to be installed along with the requests module. 

## How to use
To use this script, you must create an API user on FortiManager. Utilize the [Fortinet Docs](https://docs.fortinet.com/document/fortimanager/7.2.0/new-features/47777/fortimanager-supports-authentication-token-for-api-administrators-7-2-2) site for details.

Fill in your FortiManager FQDN in the URL section of the script.

Fill in your FortiManager ADOM the devices exist in. If ADOMs are disabled, type in root.

Put your API username and password in the script.py file under the username and password settings. 

Fill out the locationSettings.csv and vlanSettings.csv files as appropriate. 

Run the script. 

## Disclaimer
This script is provided as-is and offers no guarantee of functionality or support.