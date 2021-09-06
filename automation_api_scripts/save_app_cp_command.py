import time
import json
from cloudshell.api.cloudshell_api import CloudShellAPISession, CloudShellAPIError
import xml.etree.ElementTree as ET
import datetime

user = "admin"
password = "HVUUZ0e2FwAEyGoC5kKp"
# server = "localhost"
server = "54.200.66.175"
domain = "Global"

RESOURCE_NAME = "CentOS_ansible_test i-07997fdc8ccedb9a3"
SANDBOX_ID = "63bba51e-7a67-4ff6-bd19-4268e477513a"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

result = json.loads(api.ExecuteResourceConnectedCommand(reservationId=SANDBOX_ID,
                                                        resourceFullPath=RESOURCE_NAME,
                                                        commandName='save_app',
                                                        commandTag='remote_connectivity',
                                                        parameterValues=[],
                                                        connectedPortsFullPath=[],
                                                        printOutput=True).Output)
print(result)