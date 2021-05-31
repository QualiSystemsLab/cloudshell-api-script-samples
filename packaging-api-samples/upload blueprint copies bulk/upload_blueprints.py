from quali_api_helper import QualiApi
from timeit import default_timer
import os
import shutil
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement

TOTAL_BLUEPRINTS = 100

server = "192.168.85.40"
user = "admin"
password = "admin"
domain = "Global"


blueprint_name = "1G migration test"
base_dir_path = os.path.abspath(blueprint_name)
# bp_xml_path = "{}/Topologies/{}".format(base_dir_path, blueprint_name)
bp_xml_path = os.path.join(base_dir_path, "Topologies", blueprint_name + ".xml")

api = QualiApi(server, user, password, domain)

master_start = default_timer()

print("modifying and uploading {} blueprints:".format(TOTAL_BLUEPRINTS))
for index in range(TOTAL_BLUEPRINTS):
    unit_start = default_timer()

    # create element tree object
    tree = ET.parse(bp_xml_path)

    # get root element
    root = tree.getroot()
    details = root[0]

    # set name and alias
    details.attrib["Name"] = "{} - {}".format(blueprint_name, index + 1)
    details.attrib["Alias"] = "{} - {}".format(blueprint_name, index + 1)

    # write back to xml
    tree.write(bp_xml_path)

    # zip archive
    shutil.make_archive(blueprint_name, 'zip', base_dir_path)

    export_result = api.import_package(base_dir_path + ".zip")
    print("blueprint {} uploaded -  {} seconds".format(index + 1, default_timer() - unit_start))

print("SCRIPT DONE - {} SECONDS".format(default_timer() - master_start))