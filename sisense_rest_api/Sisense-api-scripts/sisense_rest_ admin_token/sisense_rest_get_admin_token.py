import requests  # pip install requests
from retrying import retry  # pip install retrying
import json
import time
import inspect
myself = lambda: inspect.stack()[1][3]  # utility for printing out function name in exceptions


class SisenseRest:
    def __init__(self, server, username, password, port="8081", protocol="http"):
        """
        run login command on init, attach session token to headers for subsequent requests
        :param str server:
        :param str username:
        :param str password:
        """
        self.req_session = requests.Session()
        self.server = server
        self.base_url = "{protocol}://{server}:{port}/api".format(protocol=protocol,
                                                                  server=server,
                                                                  port=port)
        self.admin_token = self._get_admin_token(username, password)
        self._set_auth_headers()

    def _get_admin_token(self, user_name, password):
        login_data = {
            "username": user_name,
            "password": password
        }
        # login is version 1.0 method (v1)
        login_url = self.base_url + "/v1/authentication/login"
        login_headers = {"Content-Type": "application/json"}
        login_res = self.req_session.post(url=login_url,
                                          data=json.dumps(login_data),
                                          headers=login_headers)
        login_data = self._handle_res_json(response=login_res, caller=myself())
        admin_token = login_data["access_token"]
        return admin_token

    def _set_auth_headers(self):
        """
        Get token from login response, then place token into auth headers on class
        """
        auth_headers = {
            'Authorization': 'Bearer {0}'.format(self.admin_token)
        }
        self.req_session.headers.update(auth_headers)

    @staticmethod
    def _handle_res_json(response, caller):
        """
        gets api response, checks status code, if passed returns json, else raises Exception
        :param response:
        :return:
        """
        if response.status_code in [200, 201, 202, 203]:
            return response.json()
        else:
            print("issue with response, status code: " + str(response.status_code))
            print response.text
            raise Exception("Failed Sisense API request from {}".format(caller))

    def get_dashboards(self):
        url = self.base_url + "/v1/dashboards"
        headers = {"Content-Type": "application/json"}
        response = self.req_session.get(url=url,
                                        headers=headers)
        if response.status_code not in [200, 201, 202, 203]:
            raise Exception("issue getting dashboards. Status code {}".format(str(response.status_code)))
        else:
            data = self._handle_res_json(response=response, caller=myself())
            return data


if __name__ == "__main__":
    with open("config.json") as config:
        data = json.load(config)

    try:
        sisense_rest = SisenseRest(server=data["sisense_server"],
                                   username=data["sisense_user"],
                                   password=data["sisense_password"],
                                   port=data["sisense_port"],
                                   protocol=data["sisense_protocol"])
    except Exception as e:
        print("issue with api session")
        raise
    else:
        print("=== Sisense Admin Token ===")
        admin_token = sisense_rest.admin_token
        print(admin_token)

        # write token to file
        with open('admin_token_output.txt', 'w') as f:
            f.write("=== Sisense Admin Token ===\n")
            f.write(admin_token)

