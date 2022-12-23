from cloudshell.api.cloudshell_api import CloudShellAPISession, AttributeNameValue

TARGET_MODEL = "Putshell"
TARGET_ATTR_KEY = "MY_ATTR"
TARGET_ATTR_VAL = "MY_VAL"

api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
target_attrs = [AttributeNameValue(TARGET_ATTR_KEY, TARGET_ATTR_VAL)]
found = api.FindResources(resourceModel=TARGET_MODEL,
                          attributeValues=target_attrs).Resources

if not found:
    raise Exception("nothing found")

for resource in found:
    print(resource.Name)

