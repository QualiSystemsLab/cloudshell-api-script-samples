from cloudshell.api.cloudshell_api import CloudShellAPISession

# add list of resources to filter for. Can use partial strings
TARGET_RESOURCES = ["mock_1"]

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


def is_resource_list_in_blueprint(api, blueprint_name, target_res_names):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param [str] target_res_names:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    bp_resources = details.Resources
    bp_resource_names = [res.Name for res in bp_resources]
    for resource_name in target_res_names:
        for bp_resource_name in bp_resource_names:
            if resource_name in bp_resource_name:
                return True
            else:
                continue


all_blueprints = api.GetTopologiesByCategory().Topologies
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_resource_list_in_blueprint(api, bp_name, TARGET_RESOURCES)]

print("=== Target Blueprints containing '{}' resources ===".format(TARGET_RESOURCES))
print(target_blueprints)

# add blueprints to text file
with open('target_blueprints.txt', 'w') as f:
    for bp in target_blueprints:
        print >> f, bp
