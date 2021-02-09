from cloudshell.api.cloudshell_api import CloudShellAPISession

# cloudshell credentials
user = "natti.k"
password = "1111"
server = "40.91.201.107"
domain = "Global"

session = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

cs_model_name = "CheckpointMgmt"
attr_name = "Create Jumpbox Shortcut"
res_name = "CheckpointMgmt"


def set_custom_attr():
    a = session.SetCustomShellAttribute(modelName=cs_model_name,
                                        attributeName=attr_name,
                                        defaultValue="True")


def remove_custom_attr():
    b = session.RemoveCustomShellAttribute(modelName=cs_model_name,
                                           attributeName=attr_name)


def set_attr_val():
    a = session.SetAttributeValue(resourceFullPath=res_name,
                                  attributeName=attr_name,
                                  attributeValue="")


def get_attr_val():
    a = session.GetAttributeValue(resourceFullPath=res_name,
                                  attributeName=attr_name)
    print("{attr} value: {val}".format(attr=a.Name, val=a.Value))


def get_service_attr_val():
    a = session.GetServices(serviceName="CheckpointMgmt")
    return a


set_custom_attr()
# remove_custom_attr()
# set_attr_val()
get_attr_val()
# get_service_attr_val()
