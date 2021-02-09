from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"

api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")

keeper_categories = ["Swisscom", "SQC", "Mobile Center Demo", "vodaphone bracknell"]
keepers = []

for category in keeper_categories:
    bps = api.GetTopologiesByCategory(category).Topologies
    keepers.extend(bps)

all_bps = api.GetTopologiesByCategory().Topologies

keepers_set = set(keepers)
all_bps_set = set(all_bps)

throw_aways = list(all_bps_set - keepers_set)

for bp in throw_aways:
    api.DeleteTopology(bp)


