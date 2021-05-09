from quali_utils.quali_packaging import PackageEditor, TopologyApp, AppResource, AppResourceInner, DeploymentService
import requests
from copy import deepcopy

# Create a new package in the local file system
package_base_path = "C:\\quali_package_demo"
# package_name = "demo_apps_blueprint.zip"
package_name = "empty_blueprint.zip"
p = PackageEditor()

package_path = "{}\\{}".format(package_base_path, package_name)

# create empty package
p.create(package_path)

# Load the package and prepare for edit
p.load(package_path)

# Edit the package: f.e add new family
# p.add_topology(topology_name="temp_blueprint", is_public="True", image_file_path="", default_duration="15",
#                instructions="", categories="", diagram_zoom="0")

topology_name = p.get_topology_names()[0]
# p.change_topology_name_and_alias(topology_name=names[0], new_name="new blueprint name")
# names_new = p.get_topology_names()

p.add_topology("my_bp", True, "", "30", "", "", "100")

apps = p.get_apps(topology_name)
app1 = apps[0]

new_app_copy = deepcopy(app1)
new_app_copy.templateName = "my template from api"
new_app_copy.appResource.name = "my temp app"


p.add_app(topology_name, new_app_copy)
pass

# ==== IMPORT PACKAGE INTO CLOUDSHELL =====
# authenticate quali api
r = requests.put('http://localhost:9000/Api/Auth/Login', {"username": "admin", "password": "admin", "domain": "Global"})
authcode = "Basic " + r._content[1:-1]

# 2 Open the package before import
fileobj = open(package_path, 'rb')

# 3 Send to CloudShell by calling Import Package REST API
r = requests.post('http://localhost:9000/API/Package/ImportPackage',
                  headers={"Authorization": authcode},
                  files={"file": fileobj})
print(r._content)
print(r.ok)