from cloudshell.api.cloudshell_api import CloudShellAPISession
from quali_api import QualiAPISession
import credentials
from update_services import update_services_flow


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("target_service")
    parser.add_argument("old_vlan")
    parser.add_argument("new_vlan")
    args = parser.parse_args()
    target_service = args.target_service
    old_vlan = args.old_vlan
    new_vlan = args.new_vlan

    my_api = CloudShellAPISession(host=credentials.HOST,
                                  username=credentials.USER,
                                  password=credentials.PASSWORD,
                                  domain=credentials.DOMAIN)
    my_quali_api = QualiAPISession(host=credentials.HOST,
                                   username=credentials.USER,
                                   password=credentials.PASSWORD,
                                   domain=credentials.DOMAIN)
    update_services_flow(my_api, my_quali_api, target_service, old_vlan, new_vlan)


if __name__ == "__main__":
    main()
