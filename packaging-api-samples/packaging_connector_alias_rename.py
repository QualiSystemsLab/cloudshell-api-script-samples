from quali_utils.quali_packaging import PackageEditor, TopologyApp, AppResource, AppResourceInner, DeploymentService


PACKAGE_PATH = r"C:\Users\natti.k\Downloads\CloudShell Sandbox Template2\CloudShell Sandbox Template2.zip"
LONG_ALIAS = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

p = PackageEditor()

p.load(PACKAGE_PATH)

bp_name = p.get_topology_names()[0]
p.add_visual_connector(topology_name=bp_name,
                       connector_alias=LONG_ALIAS,
                       resource_source_name="BlueTeam Win10",
                       resource_target_name="AppTestBase",
                       source_family_type="Resource",
                       target_family_type="Resource",
                       direction="Bi")
pass


