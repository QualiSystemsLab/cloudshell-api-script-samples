from cloudshell.api.cloudshell_api import CloudShellAPISession


def find_vm_by_uid(api, target_vm_uid):
    resources = api.FindResources(resourceFamily="Generic App Family").Resources
    resource_names = [r.Name for r in resources]
    for name in resource_names:
        details = api.GetResourceDetails(resourceFullPath=name)
        vm_details = details.VmDetails
        if not vm_details:
            continue
        vm_uid = vm_details.UID
        if vm_uid == target_vm_uid:
            return name

    raise Exception('No Deployed App Resource found with UID: {}'.format(target_vm_uid))


if __name__ == "__main__":
    user = "admin"
    password = "admin"
    server = "localhost"
    VM_ID = "4232f49f-f670-13df-5c59-8dc1b77edb66"

    api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")
    target_vm_name = find_vm_by_uid(api, VM_ID)
    print("Target VM: " + target_vm_name)