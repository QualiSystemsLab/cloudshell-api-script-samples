from cloudshell.api.cloudshell_api import CloudShellAPISession
import argparse


def clear_all_sandbox_data(api: CloudShellAPISession, sandbox_id: str) -> None:
    api.ClearSandboxData(sandbox_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("sandbox_id", help="sandbox id", type=str)
    args = parser.parse_args()
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    clear_all_sandbox_data(api, args.sandbox_id)
    print(f"sandbox data cleared for {args.sandbox_id}")
