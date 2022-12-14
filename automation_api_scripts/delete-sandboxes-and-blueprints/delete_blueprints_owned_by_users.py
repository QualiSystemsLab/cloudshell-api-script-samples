"""
The general use case here is to delete blueprints owned by a specific user
Perhaps you want to delete user from DB, or just want to remove their data
"""
import json
import sys
from typing import List
from cloudshell.api.cloudshell_api import CloudShellAPISession, TopologyInfo


def validate_cloudshell_users(api: CloudShellAPISession, users: List[str]):
    failed = []
    for curr_user in users:
        try:
            api.GetUserDetails(curr_user)
        except:
            failed.append(curr_user)
    if failed:
        raise Exception(f"Invalid cloudshell users passed:\n{json.dumps(failed, indent=4)}")


def get_regular_blueprints_owned_by_users(api: CloudShellAPISession, owners: List[str]) -> List[TopologyInfo]:
    all_blueprints = api.GetTopologiesByCategory().Topologies
    results = []
    for curr_bp in all_blueprints:
        details = api.GetTopologyDetails(topologyFullPath=curr_bp)
        if details.Type == "Regular":
            for curr_owner in owners:
                if curr_owner == details.Owner:
                    results.append(details)
    return results


def delete_user_blueprints(api: CloudShellAPISession, target_users: List[str]):
    validate_cloudshell_users(api, target_users)
    target_blueprints = get_regular_blueprints_owned_by_users(api, target_users)
    if not target_blueprints:
        print("No blueprints found. Stopping.")
        sys.exit(0)

    print("Deleting ALL blueprints owned by target users...")
    failed = []
    for curr_bp in target_blueprints:
        print(f"Deleting blueprint '{curr_bp.Name}'")
        try:
            api.DeleteTopology(topologyFullPath=curr_bp.Name)
        except Exception as e:
            print(f"Error deleting blueprint '{curr_bp.Name}'. Exception - \n{type(e).__name__}: {str(e)}")
            print("===============")
            failed.append(curr_bp.Name)

    if failed:
        raise Exception(f"Failed blueprint deletions:\n{json.dumps(failed, indent=4)}")

    print("Delete blueprints for target users script done.")


if __name__ == "__main__":
    cs_api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    target_users = ["user a", "user b"]
    delete_user_blueprints(cs_api, target_users)
