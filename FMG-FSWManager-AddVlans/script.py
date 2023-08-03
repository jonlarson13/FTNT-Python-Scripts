import requests
import json
import os
import csv


# Remove SSL warnings 
from requests.packages import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

####### Define settings for the script ####### 

# Set the URL for the FortiManager Rest API
url = "https://{url}/jsonrpc"

# Set Username/Password for the FortiManager Rest API
username = "{username}"
password = "{password}"

testline = ""

# Set the excel file to read data from
locationFile = "./FMG-FSWManager-AddVlans/locationSettings.csv" 
vlanFile = "./FMG-FSWManager-AddVlans/vlanSettings.csv"


####### end script settings ########

#####################    start functions     ######################

# FortiManager login function
def fmg_login(user,passwd):
    # Set payload in sturctured syntax
    structuredPayload = {
        "id": 1,
        "method": "exec",
        "params": [{
            "data": [{
                "passwd": passwd,
                "user": user
                }],
            "url": 
            "sys/login/user"
            }],
        "session": "null",
        "verbose": 1
    }

    # Convert payload into json format and set headers
    payload = json.dumps(structuredPayload)
    headers = {
      'Content-Type': 'text/plain'
    }

    # Execute API Call and catch result
    response = requests.request("POST", url, headers=headers, data = payload, verify=False)

    # Convert response into usable data
    json_data = json.loads(response.text)

    # If authentication is successful print sessionID
    if json_data["result"][0]["status"]["code"] == 0:
        return json_data["session"]
    else:
        return("error")

# FortiManager logout function
def fmg_logout(sessionID):
    # Set payload in structured syntax
    structuredPayload = {
        "id": 1,
        "method": "exec",
        "params": [{
            "url": "sys/logout"
            }],
        "session": sessionID,
    }

    # Convert payload into json format and set headers
    payload = json.dumps(structuredPayload)
    headers = {
      'Content-Type': 'text/plain'
    }

    # Execute API Call and catch result
    response = requests.request("POST", url, headers=headers, data = payload, verify=False)

    # Convert response into usable data
    json_data = json.loads(response.text)

    #print(json.dumps(json_data, indent=1))

    # Check if logout is successful and report status
    if json_data["result"][0]["status"]["code"] == 0:
        return("Logout successful!")
    else:
        return("Error on logout!")

 
# FortiManager FSW Device Mapping Function
def fsw_add_vlan(mappedDevice, locationID, locationIP, interfaceIp, interfaceIpMask, vlanID, vlanName, dhcpIpStart, dhcpIpEnd, sessionID):
    #set payload in structed syntax
    structuredPayload = {
        "method": "set",
        "params": [
            {
                "data": [
                    {
                        "_dhcp-status": 1,
                        "_scope": [
                            {
                                "name": mappedDevice,
                                "vdom": "root"
                            }
                        ],
                        "dhcp-server": {
                            "ip-mode": "range",
                            "ip-range": [
                                {
                                    "end-ip": str(locationIP) + "." + str(dhcpIpEnd),
                                    "start-ip": str(locationIP) + "." + str(dhcpIpStart)
                                }
                            ],
                            "lease-time": 28800,
                        },
                        "interface": {
                            "ip": [
                                str(locationIP) + "." + str(interfaceIp),
                                str(interfaceIpMask)
                            ],
                            "vlanid": str(vlanID)
                        }
                        
                    }
                ],
                "url": "/pm/config/adom/fabric/obj/fsp/vlan/" + str(vlanName) + "/dynamic_mapping"
            }
        ],
        "session": sessionID,
        "id": 1
    }

    # Convert payload into json format and set headers
    payload = json.dumps(structuredPayload)
    
    # Execute API Call and catch result
    response = requests.request("POST", url, data = payload, verify=False)

    # Convert response into usable data
    json_data = json.loads(response.text)

    # Convert response into usable data
    json_data = json.loads(response.text)
    #print(json.dumps(json_data, indent=2),"\n") #uncomment this to troubleshoot individual payloads

########################     end functions      ####################################

# Login to FortiManager 
sessionID = fmg_login(username,password)

# Loop through the list of firewalls and the csv of vlans per firewall, then call the function to add the vlans to fmg
with open(locationFile, mode ="r") as file:

    reader = csv.DictReader(file, delimiter=",")

    for locationRow in reader:
        mappedDevice=locationRow['FW-Name']
        locationID=locationRow['Location-ID']
        locationIP=locationRow['Location-IP']

        with open(vlanFile, mode="r") as file:
            reader = csv.DictReader(file, delimiter=",")

            for vlanRow in reader:
                interfaceIp=vlanRow['interfaceIp']
                interfaceIpMask=vlanRow['interfaceIpMask']
                vlanID=vlanRow['vlanID']
                vlanName=vlanRow['vlanName']
                dhcpIpStart=vlanRow['dhcpIpStart']
                dhcpIpEnd=vlanRow['dhcpIpEnd']

                 # Parse through each VLAN and create it
                createVlan = fsw_add_vlan(mappedDevice, locationID, locationIP, interfaceIp, interfaceIpMask, vlanID, vlanName, dhcpIpStart, dhcpIpEnd, sessionID)


# End FortiManager API session and print result
result = fmg_logout(sessionID)
print(result)
