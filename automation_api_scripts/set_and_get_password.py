from cloudshell.api.cloudshell_api import CloudShellAPISession

user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)

MY_STRONG_PASSWORD = "lolol"

# setting the password
api.SetAttributeValue(resourceFullPath="mock1", attributeName="Putshell.Password", attributeValue=MY_STRONG_PASSWORD)

# getting the encrypted password string from the resource
encrypted_password_val = api.GetAttributeValue(resourceFullPath="mock1", attributeName="Putshell.Password").Value
print("encrypted: " + encrypted_password_val)

# to decrypt use api
decrypted = api.DecryptPassword(encryptedString=encrypted_password_val).Value
print("decrypted: " + decrypted)

