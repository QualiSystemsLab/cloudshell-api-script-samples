"""
Generate a list of blueprints with automation api and export to a package with quali api
NOTE: shells of respective resources must be present on destination system
"""
from quali_api_wrapper import QualiAPISession
from cloudshell.api.cloudshell_api import CloudShellAPISession

# session authentication
host = "localhost"
username = "admin"
password = "admin"

# path to export your topologies package
TARGET_PATH = r"C:\Users\natti.k\Desktop\desktop_temp\demo_blueprint_package\all_blueprints.zip"

# automation api will generate a list of blueprints
auto_api = CloudShellAPISession(host=host, username=username, password=password, domain="Global")

# quali api will do the packaging operatino
quali_api = QualiAPISession(host=host, username=username, password=password)


def is_blueprint_type_template(bp_name):
    """
    check blueprint type attribute to filter for "Regular"  blueprint types
    :param str bp_name: blueprint full name
    :return:
    """
    details = auto_api.GetTopologyDetails(bp)
    if details.Type == "Template":
        return True
    else:
        return False


# get all blueprints in current api session domain by not specifying a category
all_blueprints = auto_api.GetTopologiesByCategory().Topologies

# filter for standard type blueprints
regular_blueprints = [bp for bp in all_blueprints if not is_blueprint_type_template(bp)]

res = quali_api.export_package(blueprint_full_names=regular_blueprints, target_filename=TARGET_PATH)
pass