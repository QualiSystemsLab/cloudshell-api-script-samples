import requests
from typing import List


class QualiAPISession:
    def __init__(self, host, username='', password='', domain='Global', token_id='', port=9000):
        self.session = requests.Session()
        self.base_url = f"http://{host}:{port}/Api"
        self._json_header = {"Content-Type": "application/json"}
        self.login(username, password, token_id, domain)

    def login(self, username="", password="", token_id="", domain="Global"):
        if token_id:
            body = {"Token": token_id, "Domain": domain}
        elif username and password:
            body = {"Username": username, "Password": password, "Domain": domain}
        else:
            raise ValueError("Must supply Username / Password OR a token_id")
        url = f"{self.base_url}/Auth/Login"
        login_result = requests.put(url, json=body, headers=self._json_header)
        if not login_result.ok:
            raise Exception(f"Failed Quali API login. Status {login_result.status_code}: {login_result.text}")

        # strip the extraneous quotes
        token_str = login_result.text[1:-1]
        self.session.headers.update({"Authorization": f"Basic {token_str}"})

    @staticmethod
    def _validate_response(response: requests.Response):
        if not response.ok:
            response.raise_for_status()

    def import_package(self, package_filepath: str):
        """
        Push a zipped Package file into the CloudShell Server
        provide full path to zip file
        """
        url = f"{self.base_url}/Package/ImportPackage"
        with open(package_filepath, "rb") as package_file:
            package_content = package_file.read()
            response = self.session.post(url, files={'QualiPackage': package_content})
        self._validate_response(response)

    def export_package(self, blueprint_full_names: List[str], file_path: str):
        """
        Export one or more multiple blueprints from CloudShell as a Quali Package
        pass file name to export to local dir, or full path
        """
        url = f"{self.base_url}/Package/ExportPackage"
        body = {"TopologyNames": blueprint_full_names}
        response = self.session.post(url, json=body, headers=self._json_header)
        self._validate_response(response)
        with open(file_path, "wb") as target_file:
            target_file.write(response.content)

