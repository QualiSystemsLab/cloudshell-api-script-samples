import os
import requests
import json


class QualiApiError(Exception):
    pass


class QualiAPISession:
    def __init__(self, host, username='', password='', domain='Global', token_id='', port=9000):
        self._base_url = "http://{}:{}".format(host, port)
        self.session = requests.Session()
        self.login_set_auth_header(domain, password, token_id, username)

    def login_set_auth_header(self, domain, password, token_id, username):
        if token_id:
            headers = {"token": token_id, "domain": domain}
        elif username and password:
            headers = {"username": username, "password": password, "domain": domain}
        else:
            raise ValueError("Must supply Username / Password OR token_id")
        login_result = requests.put(f"{self._base_url}/API/Auth/Login", headers)
        if not login_result.ok:
            raise QualiApiError(f"Failed API Login. Status: {login_result.status_code}. Reason: {login_result.text}")
        token_str = login_result.text[1:-1]
        auth_header = {"Authorization": f"Basic {token_str}"}
        self.session.headers.update(auth_header)

    @staticmethod
    def _validate_response(response: requests.Response):
        if not response.ok:
            raise QualiApiError(f"Failed api call. Status: {response.status_code}. Reason: {response.text}")

    def get_execution_servers(self):
        url = f"{self._base_url}/API/Manage/ExecutionServers"
        response = self.session.get(url)
        self._validate_response(response)
        return response.json()

    def get_execution_server_details(self, execution_server_name):
        url = f"{self._base_url}/API/Manage/ExecutionServers/{execution_server_name}"
        response = self.session.get(url)
        self._validate_response(response)
        return response.json()

    def get_all_server_details(self):
        all_servers = self.get_execution_servers()
        return [self.get_execution_server_details(x["Name"]) for x in all_servers]


if __name__ == "__main__":
    api = QualiAPISession("localhost", "admin", "admin", "Global")
    all_server_details = api.get_all_server_details()
    print(json.dumps(all_server_details, indent=4))
