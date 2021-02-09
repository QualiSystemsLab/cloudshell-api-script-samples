from time import sleep

from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "192.168.85.25"
# server = "localhost"
domain = "Global"

SANDBOX_ID = "ade3ca37-ac99-4bee-9496-c53cb54ed8b2"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

api.AddResourcesToReservation(reservationId=SANDBOX_ID, resourcesFullPath=["DHCp 1500"], shared=True)
api.SetReservationResourcePosition(reservationId=SANDBOX_ID, resourceFullName="DHCP 1500", x=100, y=50)
api.SetReservationServicePosition(reservationId=SANDBOX_ID, serviceAlias="Ansible Config 2G")
resource_details = api.GetResourceDetails("2G - ubuntu snapshot ansible test_d9f9-caef")
vm_details = resource_details.VmDetails
# vm_details.NetworkData[0].AdditionalData[0]
# output = api.ExecuteResourceConnectedCommand(reservationId=SANDBOX_ID,
#                                              resourceFullPath="ubuntu snapshot ansible test_1_c56b-e60e",
#                                              commandName="GetVmDetails",
#                                              commandTag="allow_unreserved",
#                                              printOutput=True).Output

output = api.ExecuteCommand(reservationId=SANDBOX_ID,
                            targetName="vcenter 110",
                            targetType="Resource",
                            commandName="GetVmDetails",
                            printOutput=True)
pass
