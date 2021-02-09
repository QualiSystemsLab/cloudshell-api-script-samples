from cloudshell.api.cloudshell_api import CloudShellAPISession
from pprint import pprint

# set list of target resources
TARGET_RESOURCE_NAME = "mock_1"

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


def is_resource_list_in_blueprint(api, blueprint_name, target_resource_name):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param str target_resource_name:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    bp_resources = details.Resources
    for curr_resource in bp_resources:
        if curr_resource.Name == target_resource_name:
            return True
    return False


all_blueprints = api.GetTopologiesByCategory().Topologies
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_resource_list_in_blueprint(api, bp_name, TARGET_RESOURCE_NAME)]

if not target_blueprints:
    print("No blueprints in system with target resource")
else:
    print("=== Target Blueprints containing '{}' ===".format(TARGET_RESOURCE_NAME))
    pprint(target_blueprints)

    # add to text file
    with open('target_blueprints.txt', 'w') as f:
        for bp in target_blueprints:
            print >> f, bp
