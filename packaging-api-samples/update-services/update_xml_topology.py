import os
import shutil
import zipfile
from etree_xml_handler import update_xml_tree


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


def edit_vlan_id_in_xml(bp_name: str, package_path: str, target_service: str, new_vlan_id: str):
    """
    1. unzip the package to temp folder
    2. clean out package for everything except Topology xml
    3. update xml tree
    4. zip up extracted folders
    5. delete temp extracted content
    """
    temp_folder = "temp_bp_extracted"

    # UNZIP PACKAGE TO TEMP FOLDER
    with zipfile.ZipFile(package_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder)

    # CLEAR OUT EVERYTHING EXCEPT TOPOLOGIES FOLDER AND METADATA XML
    _clean_bp_package(temp_folder)

    xml_path = os.path.join(temp_folder, "Topologies", f"{bp_name}.xml")
    update_xml_tree(xml_path=xml_path, target_service_model=target_service, new_vlan_id=new_vlan_id)

    # REZIP TEMP FOLDER BACK TO ZIP PACKAGE
    package_file_name = package_path.split("/")[-1].split(".zip")[0]  # handle full path and remove zip extension
    shutil.make_archive(package_file_name, 'zip', temp_folder)

    # clean up temp folder
    shutil.rmtree(temp_folder)
