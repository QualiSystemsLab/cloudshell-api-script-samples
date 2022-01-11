from cloudshell.api.cloudshell_api import CloudShellAPISession

# set domain values
SOURCE_DOMAIN = "QA"
TARGET_DOMAIN = "SE"


# start session
api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

# find resources of target model
domain_details = api.GetDomainDetails(domainName=TARGET_DOMAIN)
resources = domain_details.Resources
resource_names = [x.Name for x in resources]

blueprints = domain_details.Topologies
blueprint_names = [x.Name for x in blueprints]

# add resources
print(f"adding {len(resources)} resources")
api.AddResourcesToDomain(domainName=TARGET_DOMAIN,
                         resourcesNames=resource_names,
                         includeDecendants=True)

print("adding topologies")
api.AddTopologiesToDomain(domainName=TARGET_DOMAIN,
                          topologyNames=blueprint_names)

print("script done")
