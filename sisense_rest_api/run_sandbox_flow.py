from credentials import credentials
from sisense_rest_build_elasticube import SandboxRest

sb_rest = SandboxRest(server=credentials["server"],
                      username=credentials["username"],
                      password=credentials["password"],
                      domain=credentials["domain"])

BLUEPRINT_ID = "<Enter blueprint name or ID>"
sb_id = sb_rest.start_blueprint(blueprint_id=BLUEPRINT_ID)
