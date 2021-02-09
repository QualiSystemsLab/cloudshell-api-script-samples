from cloudshell.api.cloudshell_api import CloudShellAPISession


def _get_cp_restricted_attrs_dict(input_str):
    """

    :param str input_str:
    :return:
    """
    result = {}
    semicolon_split = input_str.split(";")
    for item in semicolon_split:
        comma_split = item.split(",")
        key = comma_split[0]
        value = comma_split[1]
        result[key] = value
    return result


def _get_restricted_pools_val(cp_attrs, target_attr):
    target_attr_search = [attr for attr in cp_attrs if attr.Name == target_attr]
    if not target_attr_search:
        raise Exception("'{}' attr not found on Cloud Provider".format(target_attr))
    resticted_attr_val = target_attr_search[0].Value
    return resticted_attr_val


def _validate_app_attr_val(api, app_resource_name, target_app_resource_model, target_attr_val):
    """

    :param CloudShellAPISession api:
    :param app_resource_name:
    :param target_attr:
    :return:
    """
    app_details = api.GetResourceDetails(app_resource_name)
    app_attrs = app_details.ResourceAttributes
    attr_search = [attr for attr in app_attrs if attr.Name == target_app_resource_model]
    if not attr_search:
        return False

    attr_val = attr_search[0].Value
    if attr_val == target_attr_val:
        return True
    else:
        return False


def validate_restricted_pools(api, cp_resource_name, cp_restricted_pools_attr, target_app_name,
                              target_app_resource_model):
    """
    :param CloudShellAPISession api:
    :param str cp_resource_name:
    :param str cp_restricted_pools_attr:
    :param ReservationAppResource app_request:
    :return:
    """
    cp_details = api.GetResourceDetails(resourceFullPath=cp_resource_name)
    cp_attrs = cp_details.ResourceAttributes
    all_generic_app_resources = api.FindResources(resourceFamily="Generic App Family").Resources

    restricted_attr_val = _get_restricted_pools_val(cp_attrs, cp_restricted_pools_attr)
    restricted_pool_dict = _get_cp_restricted_attrs_dict(restricted_attr_val)

    try:
        app_pool_limit = restricted_pool_dict[target_app_resource_model]
    except KeyError:
        return

    matching_apps = [r for r in all_generic_app_resources if r.ResourceModelName == target_app_resource_model]
    if not matching_apps:
        return

    if len(matching_apps) >= int(app_pool_limit):
        raise Exception("Can not deploy '{}'. The model '{}' has reached it's limit of {}".format(target_app_name,
                                                                                                  target_app_resource_model,
                                                                                                  app_pool_limit))


if __name__ == "__main__":
    user = "admin"
    password = "admin"
    server = "localhost"
    domain = "Global"

    # To be extracted from vCenter driver context and request objects
    CLOUD_PROVIDER_RESOURCE = "my vCenter"
    CP_RESTRICTED_POOLS_ATTR = "Restricted App Model Pools"
    TARGET_APP_MODEL = "Generic App Model Test"
    TARGET_APP_NAME = "test app name"

    api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

    validate_restricted_pools(api,
                              CLOUD_PROVIDER_RESOURCE,
                              CP_RESTRICTED_POOLS_ATTR,
                              TARGET_APP_NAME,
                              TARGET_APP_MODEL)
