from cloudshell.api.cloudshell_api import CloudShellAPISession

# set list of service "Alias"
TARGET_SERVICES = ["IxNetwork Controller"]

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)
sandboxes = api.GetCurrentReservations()
x = "lol"

def is_resource_list_in_blueprint(api, blueprint_name, target_service_names):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param [str] target_service_names:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    bp_services = details.Services
    bp_service_names = [service.Alias for service in bp_services]
    for service_name in target_service_names:
        for bp_service_name in bp_service_names:
            if service_name == bp_service_name:
                return True
            else:
                continue


all_blueprints = api.GetTopologiesByCategory().Topologies
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_resource_list_in_blueprint(api, bp_name, TARGET_SERVICES)]

if not target_blueprints:
    print("No blueprints in system with target services")
else:
    print("=== Target Blueprints containing '{}' resources ===".format(TARGET_SERVICES))
    print(target_blueprints)

    # add blueprints to text file
    with open('target_blueprints.txt', 'w') as f:
        for bp in target_blueprints:
            print >> f, bp
