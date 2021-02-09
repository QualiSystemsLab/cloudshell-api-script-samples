from cloudshell.api.cloudshell_api import CloudShellAPISession  # pip install cloudshell-automation-api


def _validate_domain_input(api, target_domain):
    """
    make sure domain exists
    :param CloudShellAPISession api:
    :param target_domain:
    :return:
    """
    try:
        api.GetDomainDetails(target_domain)
    except Exception as e:
        exc_msg = "can't get domain details for '{}': {}".format(target_domain, str(e))
        raise Exception(exc_msg)


def get_active_sandboxes_per_domain(api, target_domain):
    """
    :param CloudShellAPISession api:
    :param str target_domain:
    :return:
    """
    _validate_domain_input(api, target_domain)

    all_sandboxes = api.GetCurrentReservations().Reservations
    domain_sandboxes = [sb for sb in all_sandboxes if sb.DomainName == target_domain]

    if not domain_sandboxes:
        return
    return domain_sandboxes


if __name__ == "__main__":

    # api session details
    user = "admin"
    password = "admin"
    server = "localhost"

    # domain to search for
    TARGET_DOMAIN = "end users"

    # if command line argument passed then over ride the variable here
    import sys
    args = sys.argv
    if len(args) > 1:
        arg1 = sys.argv[1]
        TARGET_DOMAIN = arg1 if arg1 else TARGET_DOMAIN

    api = CloudShellAPISession(host=server, username=user, password=password, domain="Global")


    domain_sandboxes = get_active_sandboxes_per_domain(api, TARGET_DOMAIN)

    if not domain_sandboxes:
        print("No Current Active Sandboxes in domain '{}'".format(TARGET_DOMAIN))
        exit(0)

    print("=== Active sandboxes for domain '{}' ===".format(TARGET_DOMAIN))
    for sb in domain_sandboxes:
        print(sb.Name)

