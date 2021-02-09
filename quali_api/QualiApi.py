import os
import requests
import json


class QualiApiSession:
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
        :param blueprint_full_names: list of full Blueprint names to export (e.g. ["Folder1/Blueprint1", "Folder2/Blueprint2"])
        :param target_filename: name of the package file to create with the exported blueprints
        """
        body = {"TopologyNames": blueprint_full_names}
        export_result = self.req_session.post(url=self._api_base_url + "/Package/ExportPackage",
                                              data=json.dumps(body))
        with open(target_filename, "wb") as target_file:
            target_file.write(export_result.content)

    def get_reservation_attachment(self, sandbox_id, filename, save_path):
        """
        Download an attached file from a Sandbox. The downloaded file will be saved at {save_path}\filename
        :param sandbox_id: ID of the reservation containing the file
        :param filename: File to get from the reservation
        :param target_filename: target file name to save the file as
        """
        body = {"ReservationId": sandbox_id, "FileName": filename}
        get_result = self.req_session.post(url=self._api_base_url + "/Package/GetReservationAttachment",
                                           data=json.dumps(body))
        if 200 <= get_result.status_code < 300:
            if save_path.endswith(os.path.sep):
                with open(r"{0}{1}".format(save_path, filename), "wb") as target_file:
                    target_file.write(get_result.content)

            else:
                with open(r"{0}{1}{2}".format(save_path, os.path.sep, filename), "wb") as target_file:
                    target_file.write(get_result.content)
        else:
            raise ValueError(get_result.content)

    def get_reservation_attachment_binary(self, sandbox_id, filename):
        """
        Download an attached file from a Sandbox. The downloaded file will be saved at {save_path}\filename
        :param sandbox_id: ID of the reservation containing the file
        :param filename: File to get from the reservation
        :param target_filename: target file name to save the file as
        """
        body = {"ReservationId": sandbox_id, "FileName": filename}
        body_json = json.dumps(body)
        res = self.req_session.post(url=self._api_base_url + "/Package/GetReservationAttachment",
                                    data=body_json,
                                    headers={"Content-Type": "application/json"})
        if 200 <= res.status_code < 300:
            return res.content
        else:
            raise Exception("Rest API call to get attachment '{}' FAILED. Status code: {}".format(filename,
                                                                                                  str(
                                                                                                      res.status_code)))

    def get_reservation_attachments_details(self, sandbox_id):
        """
        Get the list of files currently attached to a Sandbox
        :param sandbox_id:
        :return: List of files attached to the Sandbox
        :rtype: list[str]
        """
        ep_url = "/Package/GetReservationAttachmentsDetails/{0}".format(sandbox_id)
        get_result = self.req_session.get(url=self._api_base_url + ep_url)
        if 200 <= get_result.status_code < 300:
            result_json = json.loads(get_result.content)
            if result_json["Success"]:
                return result_json["AllAttachments"]
            else:
                raise ValueError(result_json["ErrorMessage"])
        else:
            raise ValueError(get_result.content)

    def delete_file_from_reservation(self, sandbox_id, filename):
        """
        Delete an attached file from a Sandbox
        :param sandbox_id: The ID of the Sandbox to delete the file from
        :param filename: the exact name of the file to delete
        """
        body = {"reservationId": sandbox_id, "FileName": filename}
        delete_result = self.req_session.post(self._api_base_url + "/Package/DeleteFileFromReservation",
                                              data=json.dumps(body))

    def attach_file_to_reservation(self, sandbox_id, filename, target_filename, overwrite_if_exists=True):
        """
        Attach an existing file to a Sandbox
        :param filename: The full path of the file to attach
        :param target_filename: The name the file will be saved under in the Sandbox
        :param bool overwrite_if_exists: if True, the file will overwrite an existing file of the same name if such a file exists
        :return:
        """
        body = {
            "reservationId": sandbox_id,
            "saveFileAs": target_filename,
            "overwriteIfExists": overwrite_if_exists
        }
        with open(filename, "rb") as attached_file:
            response = self.req_session.post(url=self._api_base_url + "/Package/AttachFileToReservation",
                                             data=body,
                                             files={'QualiPackage': attached_file})
            if 200 <= response.status_code < 300:
                return response.json()
            else:
                raise Exception(
                    "Issue with attach_to_reservation api call. Status code {}. {}".format(str(response.status_code),
                                                                                           response.content))

    def write_text_to_reservation_file(self, sandbox_id, text_input, target_filename, overwrite_if_exists=True):
        """
        Write text to a file and attach file to a Sandbox
        :param filename: The full path of the file to attach
        :param target_filename: The name the file will be saved under in the Sandbox
        :param bool overwrite_if_exists: if True, the file will overwrite an existing file of the same name if such a file exists
        :return:
        """
        body = {
            "reservationId": sandbox_id,
            "saveFileAs": target_filename,
            "overwriteIfExists": overwrite_if_exists
        }

        # write text to temp file
        with open(target_filename, "w+") as attached_file:
            attached_file.write(text_input)

        # attach temp file to reservation
        with open(target_filename, "rb") as attached_file:
            response = self.req_session.post(url=self._api_base_url + "/Package/AttachFileToReservation",
                                             data=body,
                                             files={'QualiPackage': attached_file})
        # delete temp file
        os.remove(target_filename)

        if 200 <= response.status_code < 300:
            return response.json()
        else:
            raise Exception(
                "Issue with attach_to_reservation api call. Status code {}. {}".format(str(response.status_code),
                                                                                       response.content))

    def add_shell(self, shell_filename):
        """
        Add a Shell to CloudShell from a Shell Package zip file
        :param shell_filename: Full path of the Shell Package file
        :return:
        """
        with open(shell_filename, "rb") as shell_file:
            return self.req_session.post(url=self._api_base_url + "/Shells",
                                         files={"Shell": shell_file})

    def update_shell(self, shell_name, shell_filename):
        """
        Update an existing Shell in CloudShell via a Shell Package zip file
        :param shell_name: Name of the shell to update
        :param shell_filename: Full path to the Shell Package file
        :return:
        """
        with open(shell_filename, "rb") as shell_file:
            return self.req_session.put(url=self._api_base_url + "/Shells/" + shell_name,
                                        files={"Shell": shell_file})

    def get_installed_standards(self):
        """
        Acquire a list of installed CloudShell Shell standards on the CloudShell Server
        :return: The list of installed Shell Standards
        :rtype: json
        """
        get_standards_result = self.req_session.get(url=self._api_base_url + "/Standards")
        if 200 <= get_standards_result.status_code < 300:
            return get_standards_result.json()
        else:
            return get_standards_result.content

    def enqueue_job(self, job_data):
        """
        enqueue custom job
        :param job_data: The json data needed for the request
        :return: The list of installed Shell Standards
        :rtype: json
        """
        end_point = self._api_base_url + "/Scheduling/Queue"
        enqueue_job_result = self.req_session.post(url=end_point,
                                                   headers={"Content-Type": "application/json"},
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
        enqueue_suite_result = self.req_session.post(self._api_base_url + "/Scheduling/Suites",
                                                     headers={"Content-Type": "application/json"},
                                                     data=json.dumps(suite_data))
        if 200 <= enqueue_suite_result.status_code < 300:
            return enqueue_suite_result.json()
        else:
            return enqueue_suite_result.content

    def get_suite_details(self, suite_id):
        get_details_result = self.req_session.get(url=self._api_base_url + "/Scheduling/Suites/{}".format(suite_id))
        if 200 <= get_details_result.status_code < 300:
            return get_details_result.json()
        else:
            return get_details_result.content

    def get_job_details(self, job_id):
        get_details_result = self.req_session.get(url=self._api_base_url + "/Scheduling/Jobs/{}".format(job_id))
        if 200 <= get_details_result.status_code < 300:
            return get_details_result.json()
        else:
            raise Exception("Issue with job details api call. Status {}: {}".format(str(get_details_result.status_code),
                                                                                    get_details_result.content))

    def get_available_suites(self):
        get_details_result = self.req_session.get(url=self._api_base_url + "/Scheduling/SuiteTemplates")
        if 200 <= get_details_result.status_code < 300:
            return get_details_result.json()
        else:
            return get_details_result.content

    def get_running_jobs(self):
        url = self._api_base_url + "/Scheduling/Executions"
        running_jobs_res = self.req_session.get(url)
        if 200 <= running_jobs_res.status_code < 300:
            jobs = running_jobs_res.json()
            return jobs
        else:
            raise Exception(
                "Issue with get_running_jobs api call. Status code {}. {}".format(str(running_jobs_res.status_code),
                                                                                  running_jobs_res.content))


if __name__ == "__main__":
    from io import StringIO
    import paramiko
    api = QualiApiSession(host="qs-il-lt-nattik", username="admin", password="admin")
    SANDBOX_ID = "c935225f-eccb-4b0f-99c2-8c784be83193"
    # TARGET_FILENAME = "hello.txt"
    TARGET_FILENAME = "97a5d890-2675-47c4-ba01-10f1ad2d9a45.pem"
    f = open(TARGET_FILENAME)
    res = api.attach_file_to_reservation(sandbox_id=SANDBOX_ID,
                                         filename=TARGET_FILENAME,
                                         target_filename=TARGET_FILENAME,
                                         overwrite_if_exists=True)
    # res = api.write_text_to_reservation_file(sandbox_id=SANDBOX_ID,
    #                                          target_filename="test2.txt",
    #                                          text_input="take four",
    #                                          overwrite_if_exists=True)
    res = api.get_reservation_attachment_binary(SANDBOX_ID, TARGET_FILENAME)
    file_obj = StringIO(u'{}'.format(res))
    pkey = paramiko.RSAKey.from_private_key(file_obj)
    # res = api.get_installed_standards()
    # results = api.get_job_details(job_id="b8ac0f39-1d52-4437-b5e3-bcf8aecc65cf")
    pass
