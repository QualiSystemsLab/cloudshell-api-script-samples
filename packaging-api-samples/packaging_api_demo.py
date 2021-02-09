from quali_utils.quali_packaging import PackageEditor, TopologyApp, AppResource
import requests

# Create a new package in the local file system
package_base_path = "C:\\quali_package_demo"
package_name = "demo_apps_blueprint.zip"
p = PackageEditor()

package_path = "{}\\{}".format(package_base_path, package_name)

# create empty package
# p.create(package_path)

# Load the package and prepare for edit
p.load(package_path)

# Edit the package: f.e add new family
names = p.get_topology_names()
p.change_topology_name_and_alias(topology_name=names[0], new_name="new blueprint name")
names_new = p.get_topology_names()

new_app = TopologyApp()
new_app.positionX = ""
new_app.positionY = ""
new_app.templateName = ""
new_app.appResource = AppResource()
p.add_app(topology_name=names_new[0], topology_app=)
pass


# Import the package into CloudShell

# authenticate quali api

r = requests.put('http://localhost:9000/Api/Auth/Login', {"username": "admin", "password": "admin", "domain": "Global"})

authcode = "Basic " + r._content[1:-1]

# 2 Open the package before import

fileobj = open("c:\\p.zip", 'rb')

# 3 Send to CloudShell by calling Import Package REST API

r = requests.post('http://localhost:9000/API/Package/ImportPackage',

                  headers={"Authorization": authcode},

                  files={"file": fileobj})
print r._content

print r.ok