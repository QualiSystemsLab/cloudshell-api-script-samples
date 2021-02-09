from cloudshell.workflow.orchestration.sandbox import Sandbox
from custom_helpers import sb_print
from custom_helpers import get_reservation_resources
import json
import os
import requests
from quali_api_wrapper import QualiAPISession


def attach_file():
    env_vars = os.environ
    reservationContext = json.loads(os.environ["RESERVATIONCONTEXT"])
    connectivityContext = json.loads(os.environ["QUALICONNECTIVITYCONTEXT"])

    ReservationID = reservationContext["id"]
    connectivityContext["qualiAPIPort"] = "9000"
    login_result = requests.put('http://{0}:{1}/API/Auth/Login'.format(connectivityContext["serverAddress"],
                                                                       connectivityContext["qualiAPIPort"]),
                                {"username": connectivityContext["adminUser"],
                                 "password": connectivityContext["adminPass"],
                                 "domain": reservationContext["domain"]})
    authcode = "Basic " + login_result._content[1:-1]

    attached_file = open(
        r"C:\Users\natti.k\Desktop\temp\64e6ddf8-6fab-4bdf-ad7f-d9d0d8a30c0f\Cisco_IOSXR_Router_2G_1_11\ipd-zbl1313-r-bc-24--20-Jun-2018--16-48-53.log",
        'rb')

    # string to file example
    # attached_file = {'file': ('report.csv', 'some data to send')}

    attach_file_result = requests.post(
        'http://{0}:{1}/API/Package/AttachFileToReservation'.format(connectivityContext["serverAddress"],
                                                                    connectivityContext["qualiAPIPort"]),
        headers={"Authorization": authcode},
        data={"reservationId": ReservationID, "saveFileAs": "Build_Detail.txt", "overwriteIfExists": "True"},
        files={'QualiPackage': 'some test dataaaa'})

    print("The report has been attached to the reservation")


def sandbox_attach_file(sandbox, file_path, target_filename):
    q_api = QualiAPISession("localhost", "admin", "admin")
    attach_res = q_api.attach_file_to_reservation(sandbox_id=sandbox.id,
                                  filename=file_path,
                                  target_filename=target_filename,
                                  overwrite_if_exists=True)
    if attach_res.status_code == 200:
        sb_print(sandbox, "===== {file} successfully attached to sandbox =====".format(file=target_filename))

    else:
        sb_print(sandbox, "there was an issue with attaching {file}: {res_text}".format(file=target_filename,
                                                                                        res_text=attach_res.text))


def sandbox_attach_string(sandbox, input_str, target_filename):
    q_api = QualiAPISession("localhost", "admin", "admin")
    attach_res = q_api.attach_string_to_reservation(sandbox_id=sandbox.id,
                                                    input_str=input_str,
                                                    target_filename=target_filename,
                                                    overwrite_if_exists=True)

    if attach_res.status_code == 200:
        sb_print(sandbox, "{file} successfully attached to sandbox".format(file=target_filename))
    else:
        sb_print(sandbox, "there was an issue with attaching {file}: {res_text}".format(file=target_filename,
                                                                                        res_text=attach_res.text))

# ========== Primary Function ==========
def run_custom_setup(sandbox, components):
    """
    :param Sandbox sandbox:
    :param components
    :return:
    """
    # input_str = "I Am TEST STRING DATA"
    # target_filename = "string_data.txt"
    # sandbox_attach_string(sandbox, input_str, target_filename)


    file_path = r"C:\Users\natti.k\Desktop\temp\64e6ddf8-6fab-4bdf-ad7f-d9d0d8a30c0f\Cisco_IOSXR_Router_2G_1_11\ipd-zbl1313-r-bc-24--20-Jun-2018--16-48-53.log"
    target_filename = "testfile.txt"
    sandbox_attach_file(sandbox, file_path, target_filename)
