import time

from cloudshell.api.cloudshell_api import CloudShellAPISession


def create_and_autoload(api: CloudShellAPISession, resource_name: str, resource_address: str, target_model: str):
    print(f"Creating resource {resource_name}..")
    api.CreateResource(resourceName=resource_name, resourceModel=target_model, resourceAddress=resource_address)
    time.sleep(2)  # give DB a second to propagate
    print(f"autoloading resource {resource_name}...")
    api.AutoLoad(resource_name)
    print("Done.")


if __name__ == "__main__":
    TARGET_RESOURCE = "natti test resource"
    TARGET_MODEL = "Putshell"
    TARGET_ADDRESS = "1.1.1.1"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    create_and_autoload(api, TARGET_RESOURCE, TARGET_ADDRESS, TARGET_MODEL)