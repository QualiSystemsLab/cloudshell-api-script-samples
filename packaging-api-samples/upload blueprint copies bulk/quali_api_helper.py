import os
import requests
import json


class QualiApi:
    def __init__(self, host, username='', password='', domain='Global', token_id='', port=9000,
                 timezone='UTC', date_time_format='MM/dd/yyyy HH:mm'):
        self.cs_host = host
        self.username = username
        self.password = password
        self.domain = domain
        self.token_id = token_id
        self.cs_api_port = port
        self._api_base_url = "http://{0}:{1}/Api".format(host, port)
        self.req_session = requests.session()
        self._set_auth_headers()

    def _set_auth_headers(self):
        token_body = {"Token": self.token_id, "Domain": self.domain}
        creds_body = {"Username": self.username, "Password": self.password, "Domain": self.domain}
        login_headers = {"Content-Type": "application/json"}
        if self.token_id:
            login_result = requests.put(url=self._api_base_url + "/Auth/Login",
                                        data=json.dumps(token_body),
                                        headers=login_headers)
        elif self.username and self.password:
            login_result = requests.put(url=self._api_base_url + "/Auth/Login",
                                        data=json.dumps(creds_body),
                                        headers=login_headers)
        else:
            raise ValueError("Must supply either username / password OR admin token")
        if login_result.status_code not in [200, 202, 204]:
            exc_msg = "Quali API login failure. Status Code: {}. Error: {}".format(str(login_result.status_code),
                                                                                   login_result.content)
            raise Exception(exc_msg)
        auth_token = login_result.content[1:-1]
        formatted_token = "Basic {}".format(auth_token)
        auth_header = {"Authorization": formatted_token}
        self.req_session.headers.update(auth_header)
        # self.req_session.headers.update(login_headers)

    def import_package(self, package_filepath):
        """
        Import a Quali Package into the CloudShell Server
        :param package_filepath: path to the *.zip file containing the Quali Package to import
        """
        with open(package_filepath, "rb") as package_file:
            package_content = package_file.read()
            import_result = self.req_session.post(url=self._api_base_url + "/Package/ImportPackage",
                                                  files={'QualiPackage': package_content})

    def export_package(self, blueprint_full_names, target_filename):
        """
        Export one or more multiple blueprints from CloudShell as a Quali Package
        :param list[str] blueprint_full_names: list of full Blueprint names to export (e.g. ["Folder1/Blueprint1", "Folder2/Blueprint2"])
        :param target_filename: name of the package file to create with the exported blueprints
        """
        body = {"TopologyNames": blueprint_full_names}
        export_response = self.req_session.post(url=self._api_base_url + "/Package/ExportPackage",
                                              data=json.dumps(body),
                                              headers={"Content-Type": "application/json"})
        if not export_response.ok:
            raise Exception("Export failed. Status {}: {}".format(export_response.status_code,
                                                                  export_response.reason))
        with open(target_filename, "wb") as target_file:
            target_file.write(export_response.content)


if __name__ == "__main__":
    api = QualiApi("localhost", "admin", "admin", "Global")
    export_result = api.export_package(["vcenter migration dev", "L2 demo"], "test_package.zip")
    pass