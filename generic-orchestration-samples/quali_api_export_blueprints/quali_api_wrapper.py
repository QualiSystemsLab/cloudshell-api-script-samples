import os
import requests
import json


class QualiAPISession():
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

    def import_package(self, package_filepath):
        """
        Import a Quali Package into the CloudShell Server
        :param package_filepath: path to the *.zip file containing the Quali Package to import
        """
        with open(package_filepath, "rb") as package_file:
            package_content = package_file.read()
            import_result = requests.post(self._api_base_url + "/Package/ImportPackage",
                                          headers={"Authorization": self._auth_code},
                                          files={'QualiPackage': package_content})

    def export_package(self, blueprint_full_names, target_filename):
        """
        Export one or more multiple blueprints from CloudShell as a Quali Package
        :param blueprint_full_names: list of full Blueprint names to export (e.g. ["Folder1/Blueprint1", "Folder2/Blueprint2"])
        :param target_filename: name of the package file to create with the exported blueprints
        """
        url = self._api_base_url + "/Package/ExportPackage"
        headers = {"Authorization": self._auth_code, "Content-Type": "application/json"}
        body = {"TopologyNames": blueprint_full_names}

        export_result = requests.post(url=url,
                                      data=json.dumps(body),
                                      headers=headers)
        if 200 >= export_result.status_code < 300:
            with open(target_filename, "wb") as target_file:
                target_file.write(export_result.content)
        else:
            print("issue with export package api call. Response Code: {}".format(export_result.status_code))
            print(export_result.text)
            raise Exception("Export Package API issue")

    def get_reservation_attachment(self, sandbox_id, filename, save_path):
        """
        Download an attached file from a Sandbox. The downloaded file will be saved at {save_path}\filename
        :param sandbox_id: ID of the reservation containing the file
        :param filename: File to get from the reservation
        :param target_filename: target file name to save the file as
        """
        get_result = requests.post(self._api_base_url + "/Package/GetReservationAttachment",
                                   {"ReservationId": sandbox_id, "FileName": filename},
                                   headers={"Authorization": self._auth_code})
        if 200 <= get_result.status_code < 300:
            if save_path.endswith(os.path.sep):
                with open(r"{0}{1}".format(save_path, filename), "wb") as target_file:
                    target_file.write(get_result.content)

            else:
                with open(r"{0}{1}{2}".format(save_path, os.path.sep, filename), "wb") as target_file:
                    target_file.write(get_result.content)
        else:
            raise ValueError(get_result.content)

    def get_reservation_attachments_details(self, sandbox_id):
        """
        Get the list of files currently attached to a Sandbox
        :param sandbox_id:
        :return: List of files attached to the Sandbox
        :rtype: list[str]
        """
        get_result = requests.get(
            self._api_base_url + "/Package/GetReservationAttachmentsDetails/{0}".format(sandbox_id),
            headers={"Authorization": self._auth_code})
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
        delete_result = requests.post(self._api_base_url + "/Package/DeleteFileFromReservation",
                                      data={"reservationId": sandbox_id, "FileName": filename},
                                      headers={"Authorization": self._auth_code})

    def attach_file_to_reservation(self, sandbox_id, filename, target_filename, overwrite_if_exists):
        """
        Attach a file to a Sandbox
        :param filename: The full path of the file to attach
        :param target_filename: The name the file will be saved under in the Sandbox
        :param overwrite_if_exists: if True, the file will overwrite an existing file of the same name if such a file exists
        :return:
        """
        overwrite_str = "True" if overwrite_if_exists else "False"
        with open(filename, "rb") as attached_file:
            attach_file_result = requests.post(self._api_base_url + "/Package/AttachFileToReservation",
                                               headers={"Authorization": self._auth_code},
                                               data={"reservationId": sandbox_id, "saveFileAs": target_filename,
                                                     "overwriteIfExists": overwrite_if_exists},
                                               files={'QualiPackage': attached_file})




