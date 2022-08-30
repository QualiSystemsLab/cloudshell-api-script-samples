from cloudshell.api.cloudshell_api import CloudShellAPISession


class ShareStates:
    UNSHARED = "Unshared"
    SHARED = "Shared"
    FAMILY_DEFAULT = "FamilyDefault"


def _set_family_share_level(api: CloudShellAPISession, target_family, share_level):
    resources = api.FindResources(resourceFamily=target_family).Resources
    print(f"Found {len(resources)} resources")
    for resource in resources:
        try:
            api.SetResourceShareLevel(resourceFullPath=resource.Name, newShareLevel=share_level)
        except Exception as e:
            print(f"Issue processing resource {resource.Name}: {str(e)}")
    print("Done.")


def unshare_family(api: CloudShellAPISession, target_family: str):
    print(f"UNSHARING resources for family '{target_family}'")
    _set_family_share_level(api, target_family, ShareStates.UNSHARED)


def share_family(api: CloudShellAPISession, target_family: str):
    print(f"SHARING resources for family '{target_family}'")
    _set_family_share_level(api, target_family, ShareStates.SHARED)


def set_family_share_default(api: CloudShellAPISession, target_family: str):
    print(f"Setting default share level for family '{target_family}'")
    _set_family_share_level(api, target_family, ShareStates.FAMILY_DEFAULT)


if __name__ == "__main__":
    TARGET_FAMILY = "CS_SWITCH"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    unshare_family(api, TARGET_FAMILY)
