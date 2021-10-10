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

RESOURCE_NAME = "CentOS_no_config_2G_Test i-095fe8bd6200b8854"
SANDBOX_ID = "4814527a-139b-46a9-a9c5-b91d0ae33466"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

result = json.loads(api.ExecuteResourceConnectedCommand(reservationId=SANDBOX_ID,
                                                        resourceFullPath=RESOURCE_NAME,
                                                        commandName='save_app',
                                                        commandTag='remote_connectivity',
                                                        parameterValues=[],
                                                        connectedPortsFullPath=[],
                                                        printOutput=True).Output)
print(result)