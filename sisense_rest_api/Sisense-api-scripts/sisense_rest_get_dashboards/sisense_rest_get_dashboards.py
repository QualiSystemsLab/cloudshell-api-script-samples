import requests  # pip install requests
from retrying import retry  # pip install retrying
import json
import time
import inspect

myself = lambda: inspect.stack()[1][3]  # utility for printing out function name in exceptions


class SisenseRest:
    def __init__(self, server, admin_token, port="8081", protocol="http"):
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
        self._set_auth_headers(admin_token)

    def _set_auth_headers(self, admin_token):
        """
        Get token from login response, then place token into auth headers on class
        """
        auth_headers = {
            'Authorization': 'Bearer {0}'.format(admin_token)
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
    def get_jaql_data(self, jaql_json, elasticube_name="QS_Elasticube"):
        """
        get elasticube data from the server
        :return:
        """
        url = self.base_url + "/elasticubes/" + elasticube_name + "/jaql"
        headers = {"Content-Type": "application/json"}
        body = jaql_json
        response = self.req_session.post(url=url,
                                         headers=headers,
                                         data=body)
        return self._handle_res_json(response=response, caller=myself())

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

    # ===== VERSION 1.0 METHODS (http://server:port/api/v1>) =====
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
                                   admin_token=data["admin_token"],
                                   port=data["sisense_port"],
                                   protocol=data["sisense_protocol"])
    except Exception as e:
        print("=== Sisense API issue ===")
        pass
    else:
        with open("jaql_sample.json") as f:
            jaql_json = f.read()
        data = sisense_rest.get_jaql_data(jaql_json)
        print(json.dumps(data, indent=2))
        pass
        # print("=== Dashboard data ===")
        # dashboards = sisense_rest.get_dashboards()
        # print(json.dumps(dashboards, indent=2))
        # pass
