from cloudshell.api.cloudshell_api import CloudShellAPISession
import xml.etree.ElementTree as ET

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)
model_data_str = api.ExportFamiliesAndModels().Configuration
xml_data = ET.fromstring(model_data_str)