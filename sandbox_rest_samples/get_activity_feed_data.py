from credentials import credentials
from sb_rest.sandbox_rest_api import SandboxRest
import json

if __name__ == "__main__":
    SANDBOX_ID = "3eb7bbf7-6f69-4b8b-9587-aaeb196533bc"
    TARGET_TEXT = "ixia"

    sb_rest = SandboxRest(server=credentials["server"],
                          username=credentials["username"],
                          password=credentials["password"],
                          domain=credentials["domain"])

    events = sb_rest.get_sandbox_activity(SANDBOX_ID)

    filtered_events = [event for event in events
                       if TARGET_TEXT in event["event_text"]]

    events_output = json.dumps(filtered_events, sort_keys=True, indent=4)
    print(events_output)

    # generate log file
    with open('events_output.txt', 'w') as f:
        f.write("Sandbox ID: '{}', Filter for: '{}'\n".format(SANDBOX_ID, TARGET_TEXT))
        f.write(events_output)

