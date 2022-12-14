"""
Use case here is to remove all historical sandboxes where users are either owners or permitted users of that sandbox
The goal may be to then delete the users from DB, or just to remove their historical data
"""
import json
from typing import List

from cloudshell.api.cloudshell_api import ReservationShortInfo
from cloudshell.api.cloudshell_api import CloudShellAPISession


def validate_cloudshell_users(api: CloudShellAPISession, users: List[str]):
    failed = []
    for curr_user in users:
        try:
            api.GetUserDetails(curr_user)
        except Exception as e:
            failed.append(curr_user)
    if failed:
        raise Exception(f"Invalid cloudshell users passed:\n{json.dumps(failed, indent=4)}")


def get_all_historical_sandboxes(api: CloudShellAPISession, from_time: str, until_time: str) -> List[ReservationShortInfo]:
    try:
        all_sandboxes = api.GetScheduledReservations(fromTime=from_time, untilTime=until_time).Reservations
    except Exception as e:
        print(f"Issue getting sandboxes. {type(e).__name__}: {str(e)}")
        raise
    historical_sandboxes = [x for x in all_sandboxes if x.Status == "Completed"]
    return historical_sandboxes


def is_user_in_sandbox(sandbox: ReservationShortInfo, target_users: List[str]):
    if sandbox.Owner in target_users:
        return True
    for curr_user in sandbox.PermittedUsers:
        if curr_user in target_users:
            return True
    return False


def get_historical_sandboxes_with_users(api: CloudShellAPISession,
                                        target_users: List[str],
                                        from_time: str,
                                        until_time: str) -> List[ReservationShortInfo]:
    validate_cloudshell_users(api, target_users)
    all_historical_sandboxes = get_all_historical_sandboxes(api, from_time, until_time)

    if not all_historical_sandboxes:
        return []

    return [x for x in all_historical_sandboxes if is_user_in_sandbox(x, target_users)]


def delete_sandboxes_with_users(api: CloudShellAPISession, target_users: List[str], from_time: str, until_time: str):
    target_user_sandboxes = get_historical_sandboxes_with_users(api, target_users, from_time, until_time)
    if not target_user_sandboxes:
        print("no target user sandboxes found. Stopping")
        return

    print("Deleting historical sandboxes associated with target users...")
    failed = []
    for sandbox in target_user_sandboxes:
        print(f"Deleting sandbox '{sandbox.Id}'")
        try:
            api.DeleteReservation(sandbox.Id)
        except Exception as e:
            print(f"Error deleting sandbox '{sandbox.Id}'. Exception - \n{type(e).__name__}: {str(e)}")
            print("===============")
            failed.append(sandbox.Id)

    if failed:
        raise Exception(f"Failed sandbox deletions:\n{json.dumps(failed, indent=4)}")

    print("Delete sandboxes for target users done.")


if __name__ == "__main__":
    cs_api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    target_users = ["user A", "user B"]
    from_time = "01/01/2015 00:00"
    until_time = "01/01/2022 00:00"
    delete_sandboxes_with_users(cs_api, target_users, from_time, until_time)
