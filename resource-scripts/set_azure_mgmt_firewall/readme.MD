# Set Azure Virtual Appliance Routing Gateway
A utility resource script to to construct and send the API request to Azure to set routing tables on Azure

## Usage
1. Add script as resource script
2. Append resource script to desired firewall / switch model
3. Add switch / firewall to sandbox, connect subnets across the firewall / virtual appliance
4. Trigger the "set_azure_mgmt_firewall" command from setup
5. Confirm that the request worked:
   - that the routing table on Azure appears correct
   - that traffic is flowing through virtual appliance (try traceroute)
   - If issues, confirm that JSON request appears valid

## Sample request JSON structure
```json
    {
        "route_tables": [
            {
                "name": "myRouteTable1",
                "subnets": [
                    "subnetId1",
                    "subnetId2"
                ],
                "routes": [
                    {
                        "name": "myRoute1",
                        "address_prefix": "10.0.1.0/28",
                        "next_hop_type": "VirtualAppliance",
                        "next_hop_address": "10.0.1.15"
                    }
                ]
            },
            {
                "name": "myRouteTable2",
                "subnets": [
                    "subnetId3",
                    "subnetId4"
                ],
                "routes": [
                    {
                        "name": "myRoute2",
                        "address_prefix": "10.0.1.0/28",
                        "next_hop_type": "VirtualAppliance",
                        "next_hop_address": "10.0.1.15"
                    }
                ]
            }
        ]
    }
```

