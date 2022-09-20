from cloudshell.api.cloudshell_api import CloudShellAPISession


def delete_target_sandbox(api: CloudShellAPISession, sandbox_id: str):
    print(f"deleting sandbox: {sandbox_id}")
    api.DeleteReservation(reservationId=sandbox_id)
    print("done")


if __name__ == "__main__":
    TARGET_SANDBOX_ID = "c2310b47-5949-4a41-96d1-9b653338b00d"
    api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")
    delete_target_sandbox(api, TARGET_SANDBOX_ID)

