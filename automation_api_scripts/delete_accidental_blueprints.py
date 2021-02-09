from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

all_bps = api.GetTopologiesByCategory().Topologies


def is_bp_garbage(curr_bp):
    """
    filter for accdidentally made bps. Those that have template in their name but are not actually the template
    :param curr_bp:
    :return:
    """
    bp_details = api.GetTopologyDetails(curr_bp)
    if "CloudShell Sandbox Template" in bp_details.Name and bp_details.Type == "Regular":
        return True
    else:
        return False


bps_to_delete = [bp for bp in all_bps if is_bp_garbage(bp)]
for bp in bps_to_delete:
    api.DeleteTopology(bp)

pass


