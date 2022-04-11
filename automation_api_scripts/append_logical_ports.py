from cloudshell.api.cloudshell_api import CloudShellAPISession, CloudShellAPIError

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

TARGET_ROOT_RESOURCE = "my juniper"
PORT_MODEL_SUFFIX = "GenericPort"

LOGICAL_PORT_SUFFIX = "polatis_logical"
RESOURCE_EXISTS_ERROR_CODE = "114"
RESOURCE_EXISTS_ERROR = "A resource with the same name already exists"

POLATIS_LOGICAL_PORT_ATTR_NAME = "Polatis Logical Port"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)
resource_details = api.GetResourceDetails(resourceFullPath=TARGET_ROOT_RESOURCE)
root_model = resource_details.ResourceModelName
port_model = f"{root_model}.{PORT_MODEL_SUFFIX}"

chassis = resource_details.ChildResources[0]
module1 = chassis.ChildResources[0]

for i, curr_port in enumerate(module1.ChildResources):
    port_split = curr_port.Name.split("/")
    port_name = port_split[-1]
    port_path = "/".join(port_split[:-1])
    if port_name.endswith(LOGICAL_PORT_SUFFIX):
        continue

    logical_port_name = f"{port_name}_{LOGICAL_PORT_SUFFIX}"
    logical_full_path = f"{port_path}/{logical_port_name}"
    logical_address = f"{curr_port.Address}_logical"

    try:
        api.CreateResource(resourceFamily="CS_Port",
                           resourceModel=port_model,
                           resourceName=logical_port_name,
                           resourceAddress=logical_address,
                           parentResourceFullPath=module1.Name)
        print(f"created logical port {logical_port_name}")
    except CloudShellAPIError as e:
        if e.code == RESOURCE_EXISTS_ERROR_CODE:
            print(f"Port '{logical_port_name}' exists, skipping creation")

    api.SetAttributeValue(resourceFullPath=logical_full_path,
                          attributeName=POLATIS_LOGICAL_PORT_ATTR_NAME,
                          attributeValue="True")