from cloudshell.api.cloudshell_api import CloudShellAPISession


# find resources of target model
def is_blueprint_in_domain(api, bp_name):
    """
    :param CloudShellAPISession api:
    :param str bp_name:
    :return:
    """
    domain_bps = api.GetTopologiesByCategory().Topologies
    matching = [bp for bp in domain_bps if bp.split("/")[-1] == bp_name]
    return True if matching else False


if __name__ == "__main__":
    BP_NAME = "end users bp"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    print(is_blueprint_in_domain(api, BP_NAME))