from cloudshell.api.cloudshell_api import CloudShellAPISession
from dataclasses import dataclass

# cloudshell group to place users in
TARGET_GROUP = "QA users"

# Initial password - pick something more secure than this :)
DEFAULT_PASSWORD = "Quali123!"

# wheter users will be system admins or not
IS_ADMINS = False


@dataclass
class User:
    email: str
    user_name: str


api = CloudShellAPISession(host="localhost", username="admin", password="admin", domain="Global")

with open("user_emails.txt") as f:
    user_lines = [x.rstrip() for x in f.readlines()]
    user_emails = [x for x in user_lines if x]

users = []
for email in user_emails:
    split = email.split("@")
    user = User(email=email, user_name=split[0])
    users.append(user)

for user in users:
    print(f"adding user: {user.user_name}...")

    try:
        api.AddNewUser(username=user.user_name, email=user.email, password=DEFAULT_PASSWORD, isActive=True, isAdmin=IS_ADMINS)
    except Exception as e:
        print(f"issue creating user {user.user_name}. Skipping. Error: {str(e)}")
    else:
        print("user created")
        print("==========")

print("adding users to group...")
user_names = [x.user_name for x in users]
api.AddUsersToGroup(usernames=user_names, groupName=TARGET_GROUP)

print("Script Done!")


