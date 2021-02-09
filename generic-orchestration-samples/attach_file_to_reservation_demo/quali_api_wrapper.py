import requests
import os
import json


class QualiAPISession:
    def __init__(self, host, username='', password='', domain='Global', timezone='UTC', datetimeformat='MM/dd/yyyy HH:mm', token_id='', port=9000):
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
            import_result = requests.post(self._api_base_url + "/Package/ImportPackage", headers={"Authorization": self._auth_code}, files={'QualiPackage': package_content})    

    def export_package(self, blueprint_full_names, target_filename):
        """
        Export one or more multiple blueprints from CloudShell as a Quali Package
        :param blueprint_full_names: list of full Blueprint names to export (e.g. ["Folder1/Blueprint1", "Folder2/Blueprint2"])
        :param target_filename: name of the package file to create with the exported blueprints
	    """
        export_result = requests.post(self._api_base_url + "/Package/ExportPackage", {"TopologyNames": blueprint_full_names}, headers={"Authorization": self._auth_code})
        with open(target_filename, "wb") as target_file:
            target_file.write(export_result.content)

    def get_reservation_attachment(self, sandbox_id, filename, save_path):
        """
        Download an attached file from a Sandbox. The downloaded file will be saved at {save_path}\filename
        :param sandbox_id: ID of the reservation containing the file
        :param filename: File to get from the reservation
        :param target_filename: target file name to save the file as
	    """
        get_result = requests.post(self._api_base_url + "/Package/GetReservationAttachment", {"ReservationId":sandbox_id, "FileName": filename}, headers={"Authorization": self._auth_code})
        if 200 <= get_result.status_code < 300:
            if save_path.endswith(os.path.sep):
                with open(r"{0}{1}".format(save_path, filename), "wb") as target_file:
                    target_file.write(get_result.content)

            else:
                with open(r"{0}{1}{2}".format(save_path, os.path.sep, filename), "wb") as target_file:
                    target_file.write(get_result.content)
        else:
            raise ValueError(get_result.content)

    def get_reservation_attachment_details(self, sandbox_id):
        """
        Get the list of files currently attached to a Sandbox
        :param sandbox_id:
        :return: List of files attached to the Sandbox
        :rtype: list[str]
        """
        get_result = requests.get(self._api_base_url + "/Package/GetReservationAttachmentsDetails/{0}".format(sandbox_id), headers={"Authorization": self._auth_code})
        if 200 <= get_result.status_code < 300:
            result_json = json.loads(get_result.content)
            if result_json["Success"]:
                return result_json["AllAttachments"]
            else:
                raise ValueError(result_json["ErrorMessage"])
        else:
            raise ValueError(get_result.content)

    def delete_files_from_reservation(self, sandbox_id, filename):
        """
        Delete an attached file from a Sandbox
        :param sandbox_id: The ID of the Sandbox to delete the file from
        :param filename: the exact name of the file to delete
        """
        delete_result = requests.post(self._api_base_url + "/Package/DeleteFileFromReservation", data={"reservationId": sandbox_id, "FileName": filename}, headers={"Authorization": self._auth_code})

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
            attach_file_result = requests.post(self._api_base_url + "/Package/AttachFileToReservation", headers={"Authorization": self._auth_code},
										   data={"reservationId": sandbox_id, "saveFileAs": target_filename, "overwriteIfExists": overwrite_if_exists},
										   files={'QualiPackage': attached_file})

    def attach_string_to_reservation(self, sandbox_id, input_str, target_filename, overwrite_if_exists):
        """
        Attach a string to a Sandbox
        :param str sandbox_id: the current reservation id
        :param str input_str: The input string data to be written to file
        :param str target_filename: The name the file will be saved under in the Sandbox
        :param bool overwrite_if_exists: if True, the file will overwrite an existing file of the same name
        :return:
        """

        attach_file_res = requests.post(self._api_base_url + "/Package/AttachFileToReservation",
                                        headers={"Authorization": self._auth_code},
                                        data={"reservationId": sandbox_id,
                                              "saveFileAs": target_filename,
                                              "overwriteIfExists": str(overwrite_if_exists)},
                                        files={'QualiPackage': input_str})
        return attach_file_res

    def add_shell(self, shell_filename):
        """
        Add a Shell to CloudShell from a Shell Package zip file
        :param shell_filename: Full path of the Shell Package file
        :return:
	    """
        with open(shell_filename, "rb") as shell_file:
            return requests.post(self._api_base_url + "/Shells", files={"Shell": shell_file}, headers={"Authorization": self._auth_code})

    def update_shell(self, shell_name, shell_filename):
        """
        Update an existing Shell in CloudShell via a Shell Package zip file
        :param shell_name: Name of the shell to update
        :param shell_filename: Full path to the Shell Package file
        :return:
	    """
        with open(shell_filename, "rb") as shell_file:
            return requests.put(self._api_base_url + "/Shells/" + shell_name, files={"Shell": shell_file}, headers={"Authorization": self._auth_code})

    def get_installed_standards(self):
	    """
        Acquire a list of installed CloudShell Shell standards on the CloudShell Server
        :return: The list of installed Shell Standards
        :rtype: json
	    """
	    get_standards_result = requests.get(self._api_base_url + "/Standards", headers={"Authorization": self._auth_code})
	    if 200 <= get_standards_result.status_code < 300:
		    return get_standards_result.json()
	    else:
		    return get_standards_result.content
