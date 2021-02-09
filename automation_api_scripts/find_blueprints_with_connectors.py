from cloudshell.api.cloudshell_api import CloudShellAPISession

TARGET_RESOURCES = ["mock_3/Port 4", "my Cisco Switch/Chassis 0/FastEthernet0-6"]

# api session details
user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")


def is_connector_in_blueprint(api, blueprint_name, target_res_names):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param [str] target_res_names:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    connectors = details.Connectors
    if connectors:
        return True
    else:
        return False


all_blueprints = api.GetTopologiesByCategory().Topologies
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_connector_in_blueprint(api, bp_name, TARGET_RESOURCES)]

print("=== Target Blueprints containing connectors ===")
print(target_blueprints)

for bp in target_blueprints:
    api.DeleteTopology(topologyFullPath=bp)

# add blueprints to text file
# with open('target_blueprints.txt', 'w') as f:
#     for bp in target_blueprints:
#         print >> f, bp
