from cloudshell.api.cloudshell_api import CloudShellAPISession
import argparse


def get_data_key_value(api: CloudShellAPISession, sandbox_id: str, target_key: str):
    data = api.GetSandboxData(sandbox_id).SandboxDataKeyValues
    key_search = [x for x in data if x.Key == target_key]
    if not key_search:
        raise ValueError(f"Target key '{target_key}' not found in sandbox data")
    return key_search[0].Value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sandbox_id", help="sandbox id", type=str)
    parser.add_argument("key", help="target key to get value for", type=str)
    args = parser.parse_args()
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    target_value = get_data_key_value(api, args.sandbox_id, args.key)
    print(target_value)
