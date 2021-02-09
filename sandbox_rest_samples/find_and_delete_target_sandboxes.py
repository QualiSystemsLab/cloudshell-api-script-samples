from cloudshell.api.cloudshell_api import CloudShellAPISession  # pip install cloudshell-automation-api
from credentials import credentials
from sb_rest.sandbox_rest_api import SandboxRest


def is_service_in_sandbox(auto_api, sb_id, target_service_name):
    """
    for filtering sandboxes based on target service
    :param CloudShellAPISession auto_api:
    :param str sb_id:
    :param str target_service_name:
    :return:
    """
    sb_services = auto_api.GetReservationDetails(reservationId=sb_id).ReservationDescription.Services
    if not sb_services:
        return False

    for service in sb_services:
        if service.ServiceName == target_service_name:
            return True

    # if service not found return false
    return False


if __name__ == "__main__":
    TARGET_SERVICE_NAME = "IxNetwork Controller"

    server = credentials["server"]
    user = credentials["username"]
    password = credentials["password"]
    domain = credentials["domain"]

    # automation api session for getting sandbox details
    auto_api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

    # sandbox REST api for getting list of historical sandboxes
    sb_rest = SandboxRest(server=server, username=user, password=password, domain=domain)

    all_sandboxes = sb_rest.get_sandboxes(show_historic=True)
    print("total sandboxes in system: {}".format(str(len(all_sandboxes))))
    print("searching for target sandboxes...")

    filtered_sandboxes = [sb for sb in all_sandboxes
                          if is_service_in_sandbox(auto_api, sb["id"], TARGET_SERVICE_NAME)]

    if not filtered_sandboxes:
        print("NO SANDBOXES FOUND WITH TARGET SERVICE '{}'".format(TARGET_SERVICE_NAME))
    else:
        print("Service found in sandboxes, deleting...")
        for index, sandbox in enumerate(filtered_sandboxes):
            print("{}. {}".format(str(index + 1), sandbox["name"]))
            auto_api.DeleteReservation(reservationId=sandbox["id"])
