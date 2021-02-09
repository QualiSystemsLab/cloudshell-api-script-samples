from credentials import credentials
from sb_rest.sandbox_rest_api import SandboxRest
import json

if __name__ == "__main__":
    SANDBOX_ID = "b132daba-3509-4a42-ab9f-cba483cc3718"


    sb_rest = SandboxRest(server=credentials["server"],
                          username=credentials["username"],
                          password=credentials["password"],
                          domain=credentials["domain"])

    data = sb_rest.get_sandbox_data(SANDBOX_ID)
    pass
