import cloudshell.api.cloudshell_api as api
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("server")
parser.add_argument("user")
parser.add_argument("password")
parser.add_argument("resource_name")
args = parser.parse_args()

server = args.server
username = args.user
password = args.password
domain = 'Global'

# server = 'localhost'
# username = 'admin'
# password = 'admin'
# domain = 'Global'

resource_name = args.resource_name
# resource_name = 'mock_6'

session = api.CloudShellAPISession(
    username=username,
    password=password,
    domain=domain,
    host=server
)


def get_resource_user(s, res_name):
    res_details = s.GetResourceDetails(res_name)
    user_name = [attr for attr in res_details.ResourceAttributes if attr.Name == "User"][0].Value
    return user_name


def get_resource_password(s, res_name):
    res_details = s.GetResourceDetails(res_name)
    encrypted_password = [attr for attr in res_details.ResourceAttributes if attr.Type == "Password"][0].Value
    decrypted_pw = s.DecryptPassword(encrypted_password)
    return decrypted_pw.Value


def get_shell_resource_user(s, res_name):
    res_details = s.GetResourceDetails(res_name)
    resource_model = res_details.ResourceModelName
    user_attr = "{model}.User".format(model=resource_model)
    user = [attr for attr in res_details.ResourceAttributes if attr.Name == user_attr][0].Value
    return user


def get_shell_resource_password(s, res_name):
    """
    get decrypted password of target shell device
    :param Sandbox sandbox:
    :param str res_name:
    :return:
    """
    resource_details = s.GetResourceDetails(res_name)
    resource_model = resource_details.ResourceModelName
    pw_attr = "{model}.Password".format(model=resource_model)
    password_filter = [attr for attr in resource_details.ResourceAttributes if attr.Name == pw_attr]
    if password_filter:
        encrypted_pw = password_filter[0].Value
    else:
        print("no password attribute on resource: " + res_name)
        return
    decrypted_pw = s.DecryptPassword(encrypted_pw)
    return decrypted_pw.Value


# NON-NAMESPACED RESOURCE
user = get_resource_user(s=session, res_name=resource_name)
print("user: '{user}'".format(user=user))

pw = get_resource_password(s=session, res_name=resource_name)
print("password: '{pw}'".format(pw=pw))


# NAMESPACED SHELL RESOURCE
# user = get_shell_resource_user(s=session, res_name=resource_name)
# print("user: '{user}'".format(user=user))
#
# pw = get_shell_resource_password(s=session, res_name=resource_name)
# print("password: '{pw}'".format(pw=pw))

pass
