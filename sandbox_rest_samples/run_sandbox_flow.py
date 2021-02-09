from credentials import credentials
from sandbox_rest_api import SandboxRest

sb_rest = SandboxRest(server=credentials["server"],
                      username=credentials["username"],
                      password=credentials["password"],
                      domain=credentials["domain"])

BLUEPRINT_ID = "mock1 no setup"
sb_id = sb_rest.start_blueprint(blueprint_id=BLUEPRINT_ID)
print(sb_id)