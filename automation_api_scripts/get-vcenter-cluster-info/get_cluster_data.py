"""
vcenter shell command reference
https://github.com/QualiSystems/VMware-vCenter-Cloud-Provider-Shell-2G/blob/166724df98e0d6c67b16c047f8fb58de431ea4b3/src/drivermetadata.xml#L46
"""
import json

from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue
import config

api = CloudShellAPISession(host=config.SERVER,
                           username=config.USER,
                           password=config.PASSWORD,
                           domain=config.DOMAIN)

sb_details = api.GetReservationDetails(config.SANDBOX_ID, disableCache=True).ReservationDescription
resources = sb_details.Resources
deployed_apps = [x for x in resources if x.VmDetails]
cloud_provider = deployed_apps[0].VmDetails.CloudProviderFullName
command_inputs = [InputNameValue("datastore_name", config.VCENTER_DATASTORE)]
cluster_details = api.ExecuteCommand(reservationId=config.SANDBOX_ID,
                                     targetName=cloud_provider,
                                     targetType="Resource",
                                     commandName="get_cluster_usage",
                                     commandInputs=command_inputs,
                                     printOutput=True).Output
data = json.loads(cluster_details)
print(json.dumps(data, indent=4))
