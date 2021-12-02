from credentials import credentials
from sb_rest.sandbox_rest_api import SandboxRest

sb_rest = SandboxRest(server=credentials["server"],
                      username=credentials["username"],
                      password=credentials["password"],
                      domain=credentials["domain"])

BLUEPRINT_ID = "3b03d7ab-c8ac-4960-b483-42b0196e6877"
response = sb_rest.start_blueprint(blueprint_id=BLUEPRINT_ID, sandbox_name="REST testing demo")
sb_id = response["id"]
