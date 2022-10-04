"""
Usage:
python execute_command_arparse.py <SANDBOX_ID> <TEST_ID> <TEST_DATA>

Jenkins command step example:
python execute_command_arparse.py %SANDBOX_ID% "Jenkins Test Name" "Custom Data String"
"""
import argparse
from cloudshell.api.cloudshell_api import CloudShellAPISession, InputNameValue

DEFAULT_REPORTING_SERVICE_ALIAS = "Reporting Service"


def set_test_data(cs_api: CloudShellAPISession, sb_id: str, test_id: str, test_data: str):
    """
    wrapper that calls the set_test_data command on reporting service shell
    See here for command signature reference:
    https://github.com/QualiSystemsLab/CustomJobReporting-Service/blob/88403e9b714cc69101107f0dc22917173ea7b3bd/reporting-service/src/driver.py#L227
    """
    inputs = [InputNameValue("test_id", test_id),
              InputNameValue("test_data", test_data)]

    cs_api.ExecuteCommand(reservationId=sb_id,
                          targetName=DEFAULT_REPORTING_SERVICE_ALIAS,
                          targetType="Service",
                          commandName="set_test_data",
                          commandInputs=inputs,
                          printOutput=True)


if __name__ == "__main__":
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    parser = argparse.ArgumentParser()
    parser.add_argument("sandbox_id")
    parser.add_argument("test_id")
    parser.add_argument("test_data")
    args = parser.parse_args()

    set_test_data(api, args.sandbox_id, args.test_id, args.test_data)
