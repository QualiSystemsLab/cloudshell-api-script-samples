from cloudshell.api.cloudshell_api import CloudShellAPISession
from quali_api import QualiAPISession
from find_blueprints import find_blueprints_flow
from process_blueprint import process_blueprint_flow
from timeit import default_timer


def update_services_flow(api: CloudShellAPISession,
                         quali_api: QualiAPISession,
                         target_service: str,
                         old_vlan: str,
                         new_vlan: str):
    start = default_timer()
    print(f"Starting Flow. Changing service '{target_service}' VLAN {old_vlan} --> {new_vlan}")

    # find target blueprints
    target_blueprints = find_blueprints_flow(api, target_service, old_vlan)
    if not target_blueprints:
        print("No blueprints found")
        return

    # process bluperints
    for curr_bp in target_blueprints:
        process_blueprint_flow(quali_api, curr_bp, target_service, new_vlan)

    print(f"Update flow done after total {int(default_timer() - start)} seconds")


if __name__ == "__main__":
    import credentials
    import constants

    OLD_VLAN_ID = "122"
    NEW_VLAN_ID = "129"
    my_api = CloudShellAPISession(host=credentials.HOST,
                                  username=credentials.USER,
                                  password=credentials.PASSWORD,
                                  domain=credentials.DOMAIN)
    my_quali_api = QualiAPISession(host=credentials.HOST,
                                   username=credentials.USER,
                                   password=credentials.PASSWORD,
                                   domain=credentials.DOMAIN)
    update_services_flow(my_api, my_quali_api, constants.VLAN_MANUAL_SERVICE, OLD_VLAN_ID, NEW_VLAN_ID)
