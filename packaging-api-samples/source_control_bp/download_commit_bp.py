"""
1. Edit blueprint in cloudshell GUI
2. Quali API to download blueprint
3. unzip package
4. copy over files in repo and commit
"""
import os

from credentials import cs_credentials
from cloudshell.rest.api import PackagingRestApiClient
import zipfile


TARGET_BLUEPRINT = "backup test"

api = PackagingRestApiClient(ip=cs_credentials["server"],
                             port=9000,
                             username=cs_credentials["user"],
                             password=cs_credentials["password"],
                             domain=cs_credentials["domain"])

# download from quali api to local repo
response_content = api.export_package([TARGET_BLUEPRINT])
package_name = TARGET_BLUEPRINT + "_package.zip"
with open(package_name, "wb") as target_file:
    target_file.write(response_content)

curr_dir = os.getcwd()
package_path = os.path.join(curr_dir, package_name)
unzipped_dir = "{}_package_unzipped".format(TARGET_BLUEPRINT)
unzipped_path = os.path.join(curr_dir, unzipped_dir)
with zipfile.ZipFile(package_path, 'r') as zip_ref:
    zip_ref.extractall(unzipped_path)












