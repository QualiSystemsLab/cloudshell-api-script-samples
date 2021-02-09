import pandas as pd
from cloudshell.api.cloudshell_api import CloudShellAPISession
from cloudshell.api.common_cloudshell_api import CloudShellAPIError

# CLOUDSHELL SESSION CREDENTIALS
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

# EXCEL DETAILS
EXCEL_FILENAME = "user_emails.xlsx"
COLUMN_NAME = "user_mails"

# SCRIPT DETAILS
TARGET_GROUP = "mock_users_group"

df = pd.read_excel(EXCEL_FILENAME, sheet_name=0) # can also index sheet by name or fetch all sheets
user_email_list = df[COLUMN_NAME].tolist()


api = CloudShellAPISession(host=server,
                           username=user,
                           password=password,
                           domain=domain)

# ADD NEW USERS TO SYSTEM, SKIP IF ALREADY EXIST
print("adding users...")
for user_mail in user_email_list:
    try:
        api.AddNewUser(username=user_mail,
                       password="default",
                       email=user_mail,
                       isActive=True)
    except CloudShellAPIError:
        print("'{}' already exists, skipping creation".format(user_mail))

# CREATE GROUP, SKIP IF IT EXISTS
print("creating group '{}'".format(TARGET_GROUP))
try:
    api.AddNewGroup(groupName=TARGET_GROUP,
                    description="a mock group for demo purposes",
                    groupRole="Regular")
except CloudShellAPIError:
    print("'{}' already exists, skipping creation".format(TARGET_GROUP))

# ADD USERS TO GROUP
print("adding users to '{}' group...".format(TARGET_GROUP))
api.AddUsersToGroup(usernames=user_email_list,
                    groupName=TARGET_GROUP)