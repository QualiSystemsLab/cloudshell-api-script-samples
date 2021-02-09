from cloudshell.api.cloudshell_api import CloudShellAPISession


def _get_target_attr_obj(api, resource_name, target_attr_name):
    """
    get attribute "object" {Name, Value} on resource
    Includes validation for 2nd gen shell namespace by pre-fixing family/model namespace
    :param CloudShellAPISession api:
    :param str resource_name:
    :param str target_attr_name: the name of target attribute. Do not include the prefixed-namespace
    :return attribute object or None:
    """
    res_details = api.GetResourceDetails(resource_name)
    res_model = res_details.ResourceModelName
    res_family = res_details.ResourceFamilyName

    # Attribute names with 2nd gen name space (using family or model)
    target_model_attr = "{model}.{attr}".format(model=res_model, attr=target_attr_name)
    target_family_attr = "{family}.{attr}".format(family=res_family, attr=target_attr_name)

    # check against all 3 possibilities
    target_res_attr_filter = [attr for attr in res_details.ResourceAttributes if attr.Name == target_attr_name
                              or attr.Name == target_model_attr
                              or attr.Name == target_family_attr]
    if target_res_attr_filter:
        return target_res_attr_filter[0]
    else:
        return None


def get_resource_attr_val(api, resource_name, target_attr_name):
    """
    Get value of attribute if it exists
    :param CloudShellAPISession api:
    :param str resource_name:
    :param str target_attr_name:
    :return:
    """
    target_attr_obj = _get_target_attr_obj(api, resource_name, target_attr_name)
    if target_attr_obj:
        return target_attr_obj.Value
    else:
        return None


def get_decrypted_attr_val(api, resource_name, target_attr):
    """
    get the decrypted password of a resource
    :param CloudShellAPISession api:
    :param str resource_name:
    :return:
    """
    encrypted_pw = get_resource_attr_val(api, resource_name, target_attr)
    decrypted_pw = api.DecryptPassword(encrypted_pw)
    if decrypted_pw:
        return decrypted_pw.Value
    else:
        return None


def get_resource_credentials(api, resource_name):
    """
    Get Resource User and Decrypted Password Credentials as a dictionary {User, Password}
    :param CloudShellAPISession api:
    :param str resource_name:
    :return:
    """
    user = get_resource_attr_val(api, resource_name, "User")
    pw = get_decrypted_attr_val(api, resource_name, "Password")
    return user, pw


def get_resource_passwords(api, resource_name):
    enable_password = get_decrypted_attr_val(api, resource_name, "Enable Password")
    snmp_read_community = get_decrypted_attr_val(api, resource_name, "SNMP Read Community")
    snmp_write_community = get_decrypted_attr_val(api, resource_name, "SNMP Write Community")
    snmp_v3_password = get_decrypted_attr_val(api, resource_name, "SNMP V3 Password")
    backup_password = get_decrypted_attr_val(api, resource_name, "Backup Password")
    console_password = get_decrypted_attr_val(api, resource_name, "Console Password")

    result = {
        "enable_password": enable_password,
        "snmp_read_community": snmp_read_community,
        "snmp_write_community": snmp_write_community,
        "snmp_v3_password": snmp_v3_password,
        "backup_password": backup_password,
        "console_password": console_password
    }
    return result


if __name__ == "__main__":
    TARGET_RESOURCE = "virtual juniper switch"
    api = CloudShellAPISession("130.61.107.253", "quali_natti", "1111", "Global")
    user, pw = get_resource_credentials(api, TARGET_RESOURCE)
    print(pw)
    pass




































