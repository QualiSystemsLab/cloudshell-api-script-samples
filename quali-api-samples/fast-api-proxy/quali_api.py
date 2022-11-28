import json

import requests
from requests import Response


class QualiAPIHandler:
    def __init__(self, host, port=9000):
        self._base_url = f"http://{host}:{port}/Api"

    def login(self, user_name: str = None, password: str = None, domain: str = "Global") -> Response:
        headers = {"username": user_name, "password": password, "domain": domain}
        return requests.put(f"{self._base_url}/Auth/Login", headers)

    @staticmethod
    def get_token_from_login(response: Response):
        return response.text[1:-1]

    @staticmethod
    def _prep_auth_header(token):
        return f"Basic {token}"

    def get_available_suites(self, token) -> dict:
        response = requests.get(self._base_url + "/Scheduling/SuiteTemplates",
                                headers={"Authorization": self._prep_auth_header(token)})
        if not response.ok:
            response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    # sanity test
    api = QualiAPIHandler("localhost")
    token = api.login(user_name="admin", password="admin", domain="Global")
    suites = api.get_available_suites(token)
    print(json.dumps(suites, indent=4))
    pass
