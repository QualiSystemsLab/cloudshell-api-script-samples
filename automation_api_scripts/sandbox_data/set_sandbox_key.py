from cloudshell.api.cloudshell_api import CloudShellAPISession, SandboxDataKeyValue
import argparse


def set_data_key_value(api: CloudShellAPISession, sandbox_id: str, key: str, value: str) -> None:
    api.SetSandboxData(sandbox_id, [SandboxDataKeyValue(key, value)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sandbox_id", help="sandbox id", type=str)
    parser.add_argument("key", help="target key to get value for", type=str)
    parser.add_argument("value", help="target value to set on key", type=str)
    args = parser.parse_args()
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    set_data_key_value(api, args.sandbox_id, args.key, args.value)
