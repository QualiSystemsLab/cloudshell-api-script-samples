from cloudshell.api.cloudshell_api import CloudShellAPISession
from typing import List
from timeit import default_timer


def find_blueprints_flow(api: CloudShellAPISession, target_service_name: str, old_vlan: str) -> List[str]:
    print("starting blueprint search")
    start = default_timer()
    all_blueprints = api.GetTopologiesByCategory().Topologies
    print(f"System Blueprint Count: {len(all_blueprints)}")

    target_blueprints = []
    for blueprint in all_blueprints:
        services = api.GetTopologyDetails(blueprint).Services
        for curr_service in services:
            if curr_service.ServiceName == target_service_name:
                attrs = curr_service.Attributes
                vlan_id = [x for x in attrs if x.Name == "VLAN ID"][0].Value
                if vlan_id == old_vlan:
                    print(f"found target blueprint {blueprint}")
                    target_blueprints.append(blueprint)
                    break
    print(f"Target blueprints found: {len(target_blueprints)}")
    print(f"search done after {int(default_timer() - start)} seconds")
    # need only the blueprint name for quali api, not the full path
    return [x.split("/")[-1] for x in target_blueprints]


if __name__ == "__main__":
    import credentials
    import constants

    OLD_VLAN = "43"
    api = CloudShellAPISession(host=credentials.HOST,
                               username=credentials.USER,
                               password=credentials.PASSWORD,
                               domain=credentials.DOMAIN)
    found = find_blueprints_flow(api, constants.VLAN_MANUAL_SERVICE, OLD_VLAN)
    print(f"found: {found}")
