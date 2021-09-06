from build_app_xml import app_template
from upload_to_cloudshell import upload_app_to_cloudshell

# deploy_paths = [
#     {
#         "name": "my deployment path 1",
#         "is_default": True,
#         "service_name": "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G",
#         "attributes": {
#             "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM": "Natti.k\Clones\Ubuntu-18",
#             "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot": "clean_snap",
#         }
#     },
#     {
#         "name": "my deployment path 2",
#         "is_default": False,
#         "service_name": "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G",
#         "attributes": {
#             "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM": "Natti.k\Clones\Ubuntu-18",
#             "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot": "clean_snap",
#         }
#     }
# ]

deploy_paths = [
    {
        "name": "my deployment path 1",
        "is_default": True,
        "service_name": "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G",
        "attributes": {
            "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM": "Natti.k\Clones\Ubuntu-18",
            "VMware vCenter Cloud Provider 2G.vCenter VM From Linked Clone 2G.vCenter VM Snapshot": "clean_snap",
        }
    }
]

app_attributes = {
    "App Deploy Order": "N/A",
    "Execution Server Selector": "my ES"
}

# CREATE APP XML
app_xml = app_template(app_name="test asdf",
                       deploy_paths=deploy_paths,
                       categories=["category1", "category 2"],
                       app_attributes=app_attributes,
                       model="Generic App Model",
                       driver="",
                       cloud_provider="my vcenter 2G",
                       image_name="vm.png")

# UPLOAD APP TEMPLATE
upload_app_to_cloudshell(app_name="my api app test",
                         app_xml_content=app_xml,
                         server="localhost",
                         user="admin",
                         password="admin")
