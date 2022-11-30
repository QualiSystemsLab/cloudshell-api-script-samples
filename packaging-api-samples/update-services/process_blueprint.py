import os

import update_package
import update_xml_topology
from quali_api import QualiAPISession
from timeit import default_timer


def process_blueprint_flow(quali_api: QualiAPISession, blueprint_name: str, target_service: str, new_vlan_id: str):

    print(f"processing blueprint {blueprint_name}")
    start = default_timer()

    # download package
    zip_name = f"{blueprint_name}.zip"
    quali_api.export_package(blueprint_full_names=[blueprint_name],
                             file_path=zip_name)

    # with packaging api, commented out to remove dependency
    # update_package.edit_vlan_id_in_package(zip_name, target_service, new_vlan_id)

    # with Etree xml manipulation
    update_xml_topology.edit_vlan_id_in_xml(bp_name=blueprint_name,
                                            package_path=zip_name,
                                            target_service=target_service,
                                            new_vlan_id=new_vlan_id)

    # re-upload
    quali_api.import_package(zip_name)

    # delete zip archive
    os.remove(zip_name)
    print(f"done processing {blueprint_name} after {int(default_timer() - start)} seconds")


if __name__ == "__main__":
    import credentials
    import constants
    TARGET_BLUEPRINT = "vlan dev"
    NEW_VLAN_ID = "122"
    api = QualiAPISession(host=credentials.HOST,
                          username=credentials.USER,
                          password=credentials.PASSWORD,
                          domain=credentials.DOMAIN)
    process_blueprint_flow(api, TARGET_BLUEPRINT, constants.VLAN_MANUAL_SERVICE, NEW_VLAN_ID)
