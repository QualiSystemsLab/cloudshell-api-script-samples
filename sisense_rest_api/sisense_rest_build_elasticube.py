import requests  # pip install requests
from retrying import retry  # pip install retrying
import json
import time
import inspect
myself = lambda: inspect.stack()[1][3]  # utility for printing out function name in exceptions

# add sisense credentials
SISENSE_SERVER = "localhost"
SISENSE_USER = "<USER>"
SISENSE_PASSWORD = "<PASSWORD>"
ELASTICUBE_NAME = 'QS_ElastiCube'


class SisenseRest:
    def __init__(self, server, username, password, port="8083", protocol="http"):
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
        self._set_auth_headers(username, password)

    def _set_auth_headers(self, user_name, password):
        """
        Get token from login response, then place token into auth headers on class
        """
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
        login_token = login_data["access_token"]
        auth_headers = {
            'Authorization': 'Bearer {0}'.format(login_token)
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

    # ===== VERSION 0.9 METHODS (http://server:port/api/<endpoint>) =====
    def _get_elasticube_data(self, elasticube_name=""):
        """
        get elasticube data from the server
        :return:
        """
        url = self.base_url + "/elasticubes/servers/" + self.server
        headers = {"Content-Type": "application/json"}
        response = self.req_session.get(url=url,
                                        headers=headers,
                                        params={'q': elasticube_name})
        return self._handle_res_json(response=response, caller=myself())

    def _get_elasticube_id_from_name(self, elasticube_name):
        ec_data = self._get_elasticube_data(elasticube_name=elasticube_name)
        if ec_data:
            return ec_data[0]["_id"]
        else:
            raise Exception("could not find target elasticube '{}' - Please check spelling (case sensitive)".format(
                elasticube_name))

    def _get_elasticube_status(self, elasticube_name=""):
        """
        get elasticube data from the server
        :return:
        """
        url = self.base_url + "/elasticubes/servers/" + self.server + "/status"
        headers = {"Content-Type": "application/json"}
        response = self.req_session.get(url=url,
                                        headers=headers,
                                        params={'q': elasticube_name})
        data = self._handle_res_json(response=response, caller=myself())
        if data:
            return data[0]["status"]
        else:
            raise Exception("could not find target elasticube '{}' - Please check spelling (case sensitive)".format(
                elasticube_name))

    def build_elasticube(self, elasticube_name, build_type='full'):
        ec_id = self._get_elasticube_id_from_name(elasticube_name)
        url = self.base_url + "/elasticubes/" + self.server + "/" + ec_id + "/startBuild"
        headers = {"Content-Type": "application/json"}
        response = self.req_session.post(url=url,
                                         headers=headers,
                                         params={'type': build_type})
        if response.status_code not in [200, 201, 202, 203]:
            raise Exception("issue starting elasticube. Status code {}".format(str(response.status_code)))

    def poll_build_status(self, elasticube_name, max_polling_in_minutes=15, polling_frequency_in_seconds=30):
        def build_status_validation(build_status):
            if build_status == 1:
                print("Build Status 1: Cube is Stopped")
                print("==========")
                return False
            elif build_status == 2:
                print("Build Status 2: Cube is Running")
                print("==========")
                return False
            else:
                print("polling build status... status: " + str(build_status))
                return True

        # retry wait times are in milliseconds
        @retry(retry_on_result=build_status_validation, wait_fixed=polling_frequency_in_seconds * 1000,
               stop_max_delay=max_polling_in_minutes * 60000)
        def get_build_status(ec_name):
            return self._get_elasticube_status(ec_name)

        get_build_status(elasticube_name)


if __name__ == "__main__":
    sisense_rest = SisenseRest(server=SISENSE_SERVER, username=SISENSE_PASSWORD, password=SISENSE_PASSWORD)
    sisense_rest.build_elasticube(ELASTICUBE_NAME)
    print("starting build... wait 90 seconds to initialize before polling")
    time.sleep(90)
    print("====== begin polling build state ======")
    sisense_rest.poll_build_status(ELASTICUBE_NAME)
