from cloudshell.api.cloudshell_api import CloudShellAPISession

TARGET_RESOURCES = ["mock_3/Port", "myXena/Module0"]

# api session details
user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")


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


all_categories = api.GetTopologyCategories().Categories
all_blueprints = set()
for category in all_categories:
    bps = api.GetTopologiesByCategory(categoryName=category).Topologies
    all_blueprints.update(bps)
all_blueprints = list(all_blueprints)
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_resource_list_in_blueprint(api, bp_name, TARGET_RESOURCES)]

print("=== Target Blueprints containing '{}' resources ===".format(TARGET_RESOURCES))
print(target_blueprints)

# add blueprints to text file
with open('target_blueprints.txt', 'w') as f:
    for bp in target_blueprints:
        print >> f, bp
