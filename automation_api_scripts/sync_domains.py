from cloudshell.api.cloudshell_api import CloudShellAPISession

# can extend this list with more objects to manage additional domains
domain_data = [
    {
        "domain": "test_sync_domain",
        "blueprint": "physical connections demo"
    }
]

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


def validate_resources(api, resource_name):
    """
    this method is used for filtering out mid level structures that are in a domain but not explicitly in a blueprint
    removing a mid level structure would remove all the child resources below it
    :param api:
    :param resource_name:
    :return:
    """
    child_resources = api.GetResourceDetails(resourceFullPath=resource_name).ChildResources
    if child_resources:
        return False
    else:
        return True
    pass


def sync_domain(api, curr_domain, curr_blueprint):
    """
    uses the strategy of comparing the difference between blueprint and domain resource sets in order to sync
    :param api:
    :param curr_domain:
    :param curr_blueprint:
    :return:
    """
    # get blueprint resources
    # res_details = api.GetResourceDetails(resourceFullPath="my Cisco Switch/Chassis 0")
    bp_resources = api.GetTopologyDetails(curr_blueprint).Resources
    bp_resource_names = {resource.Name for resource in bp_resources}

    # get domain resources
    domain_resources = api.GetDomainDetails(domainName=curr_domain).Resources
    domain_resource_names = {resource.Name for resource in domain_resources}

    # get difference between sets
    resources_to_add = bp_resource_names - domain_resource_names
    resources_to_remove = domain_resource_names - bp_resource_names
    # Do not want to remove mid level structure resources from domain that may not be explicitly in blueprint
    validated_resources_to_remove = {resource_name for resource_name in resources_to_remove
                                     if validate_resources(api, resource_name)}

    if resources_to_add:
        api.AddResourcesToDomain(domainName=curr_domain, resourcesNames=list(resources_to_add))
        print("added resources to domain: '{}'".format(curr_domain))
        print(str(resources_to_add))
        print("===========")

    if validated_resources_to_remove:
        api.RemoveResourcesFromDomain(domainName=curr_domain, resourcesNames=list(validated_resources_to_remove))
        print("removed resources from domain '{}'".format(curr_domain))
        print(str(resources_to_remove))
        print("===========")


for data in domain_data:
    sync_domain(api=api, curr_domain=data["domain"], curr_blueprint=data["blueprint"])