from _quali_api_wrapper import QualiAPISession
import json

# quali api credentials
# host = "localhost"
# username = "admin"
# password = "admin"

host = "172.40.0.215"
username = "Administrator"
password = "Do@Quali"

api = QualiAPISession(host=host, username=username, password=password)
suites = api.get_available_suites()

for suite in suites:
    print(json.dumps(suite, sort_keys=True, indent=4))
