from cloudshell.api.cloudshell_api import CloudShellAPISession
from pprint import pprint
from timeit import default_timer

# set list of target resources
TARGET_CLOUD_PROVIDER_RESOURCE = "my vcenter 2G"

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


def is_resource_list_in_blueprint(api, blueprint_name, target_cloud_provider):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param str target_cloud_provider:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    bp_apps = details.Apps
    for curr_app in bp_apps:
        deployment_paths = curr_app.DeploymentPaths
        for dp in deployment_paths:
            curr_cloud_provider = dp.DeploymentService.CloudProvider
            if curr_cloud_provider == target_cloud_provider:
                return True
    return False

start = default_timer()
all_blueprints = api.GetTopologiesByCategory().Topologies

print("searching {} blueprints for results...".format(len(all_blueprints)))

target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_resource_list_in_blueprint(api, bp_name, TARGET_CLOUD_PROVIDER_RESOURCE)]

if not target_blueprints:
    print("No blueprints in system with target resource")
else:
    print("=== Target Blueprints containing '{}' ===".format(TARGET_CLOUD_PROVIDER_RESOURCE))
    pprint(target_blueprints)

    # add to text file
    with open('target_blueprints.txt', 'w') as f:
        for bp in target_blueprints:
            print >> f, bp

print("Done after {} seconds.".format(default_timer() - start))
