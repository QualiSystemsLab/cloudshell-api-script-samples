import os
import shutil
import zipfile
from quali_utils.quali_packaging import PackageEditor
import constants


def _clean_bp_package(base_path: str):
    """
    clean out unwanted folders
    """
    dir_contents = os.listdir(base_path)
    for item in dir_contents:
        if item.endswith(".xml"):
            continue
        if item == "Topologies":
            continue
        full_path = os.path.join(base_path, item)
        shutil.rmtree(full_path)


def _clean_bp_archive(package_path: str):
    """
    1. unzip the package
    2. clean out package for everything except Topology xml
    3. zip everything back up
    """
    temp_folder = "temp_bp_extracted"

    # UNZIP PACKAGE TO TEMP FOLDER
    with zipfile.ZipFile(package_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)

    # CLEAR OUT EVERYTHING EXCEPT APP TEMPLATES AND METADATA XML
    _clean_bp_package(temp_folder)

    # REZIP TEMP FOLDER BACK TO ZIP PACKAGE
    package_file_name = package_path.split("/")[-1].split(".zip")[0]  # handle full path and remove zip extension
    shutil.make_archive(package_file_name, 'zip', temp_folder)

    # clean up temp folder
    shutil.rmtree(temp_folder)


def edit_vlan_id_in_package(package_path: str, target_service: str, new_vlan_id: str):
    _clean_bp_archive(package_path)
    p = PackageEditor()
    p.load(package_path)
    bp_names = p.get_topology_names()
    if len(bp_names) > 1:
        raise ValueError("This script assumes only one blueprint per package")
    bp_name = bp_names[0]
    p.set_attribute_to_service(topology_name=bp_name,
                               service_alias=target_service,
                               attribute_name=constants.VLAN_ID_ATTR,
                               attribute_value=new_vlan_id,
                               publish=False)


if __name__ == "__main__":
    TARGET_PACKAGE = "vlan dev.zip"
    TARGET_SERVICE = "VLAN Manual"
    edit_vlan_id_in_package(TARGET_PACKAGE, TARGET_SERVICE, "42")
