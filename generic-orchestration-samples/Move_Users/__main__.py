import cloudshell.api.cloudshell_api as api

username = 'admin'
password = 'admin'
server = 'localhost'
domain = 'Global'
new_server = 'localhost'

session = api.CloudShellAPISession(
    username=username,
    password=password,
    domain=domain,
    host=server
)


def move_from_external(ldap_list, target_group):
    """
    :param list[str] ldap_list: the list received from LDAP directory
    :param str target_group: the group where the users will be moved
    :return:
    """
    # obtaining list of user names in cloudshell group named 'external'
    groups = session.GetGroupsDetails().Groups
    external_group_users = [group.Users for group in groups if group.Name == "external"][0]
    external_group_names = [user.Name for user in external_group_users]

    # creating list of names that occur in both ldap and cloudshell 'external' lists
    matching_set = set(ldap_list).intersection(external_group_names)
    matching_list = list(matching_set)

    # add matching users to different group and remove from 'external'
    session.AddUsersToGroup(usernames=matching_list, groupName=target_group)
    session.RemoveUsersFromGroup(usernames=external_group_names, groupName='external')


ldap_mock_users = ["mock user 1", "mock user 2", "mock user 3", "mock user 4", "mock user 5", "mock user 6", "mock user 7"]




userdata = [{'name': "test_group", 'groups': ['group 1', 'group 2']}]
# move_from_external(ldap_list=ldap_mock_users, target_group='abc')


# ==================== Test Reset ==========================
def test_reset():
    reset_users = ["mock user 1", "mock user 2", "mock user 3", "mock user 4", "mock user 5"]
    session.AddUsersToGroup(usernames=reset_users, groupName='external')
    session.RemoveUsersFromGroup(usernames=reset_users, groupName='abc')


# test_reset()

all_cs_users = session.GetAllUsersDetails()
print(len(all_cs_users))

