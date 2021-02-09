import os
import json

import requests  # pip install requests


class QualiApiSession():
    def __init__(self, host, username='', password='', domain='Global', timezone='UTC',
                 datetimeformat='MM/dd/yyyy HH:mm', token_id='', port=9000):
        self._api_base_url = "http://{0}:{1}/Api".format(host, port)
        if token_id:
            login_result = requests.put(self._api_base_url + "/Auth/Login", {"token": token_id, "domain": domain})
        elif username and password:
            login_result = requests.put(self._api_base_url + "/Auth/Login",
                                        {"username": username, "password": password, "domain": domain})
        else:
            raise ValueError("Must supply either username and password or token_id")
        self._auth_code = "Basic {0}".format(login_result.content[1:-1])

    def enqueue_job(self, job_data):
        """
        enqueue custom job
        :param job_data: The json data needed for the request
        :return: The list of installed Shell Standards
        :rtype: json
        """
        end_point = self._api_base_url + "/Scheduling/Queue"
        enqueue_job_result = requests.post(url=end_point,
                                           headers={"Authorization": self._auth_code,
                                                    "Content-Type": "application/json"},
                                           data=json.dumps(job_data))
        if 200 <= enqueue_job_result.status_code < 300:
            return enqueue_job_result.json()
        else:
            return enqueue_job_result.content

    def enqueue_suite(self, suite_data):
        """
        enqueue custom job
        :return: The list of installed Shell Standards
        :rtype: json
        """
        enqueue_suite_result = requests.post(self._api_base_url + "/Scheduling/Suites",
                                             headers={"Authorization": self._auth_code,
                                                      "Content-Type": "application/json"},
                                             data=json.dumps(suite_data))
        if 200 <= enqueue_suite_result.status_code < 300:
            return enqueue_suite_result.json()
        else:
            return enqueue_suite_result.content

    def get_suite_details(self, suite_id):
        get_details_result = requests.get(self._api_base_url + "/Scheduling/Suites/{}".format(suite_id),
                                          headers={"Authorization": self._auth_code})
        if 200 <= get_details_result.status_code < 300:
            return get_details_result.json()
        else:
            return get_details_result.content

    def get_available_suites(self):
        get_details_result = requests.get(self._api_base_url + "/Scheduling/SuiteTemplates",
                                          headers={"Authorization": self._auth_code})
        if 200 <= get_details_result.status_code < 300:
            return get_details_result.json()
        else:
            return get_details_result.content

    def get_running_jobs(self):
        url = self._api_base_url + "/Scheduling/Executions"
        running_jobs_res = requests.get(url, headers={"Authorization": self._auth_code})
        if 200 <= running_jobs_res.status_code < 300:
            jobs = running_jobs_res.json()
            return jobs
        else:
            return running_jobs_res.content


if __name__ == "__main__":
    api = QualiApiSession(host="localhost",
                          username="admin",
                          password="admin",
                          domain="Global")
    running_jobs = api.get_running_jobs()  # if no jobs, returns empty list
    if running_jobs:
        print(json.dumps(running_jobs, indent=4))
    else:
        print("no jobs running")