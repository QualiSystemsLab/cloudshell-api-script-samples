from time import sleep

from cloudshell.api.cloudshell_api import CloudShellAPISession
import xmltodict

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

SANDDBOX_ID = "37170584-46a5-4634-91aa-54c50e13b552"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

group_details = api.GetGroupsDetails()
pass


