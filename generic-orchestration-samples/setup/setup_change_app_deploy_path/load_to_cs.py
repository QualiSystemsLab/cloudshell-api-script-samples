import zipfile
import cloudshell.api.cloudshell_api as cs_api
import os

# ***************Set session credentials***********************

server_host = 'localhost'
user_name = 'admin'
password = 'admin'
domain = 'Global'

# ***************Add Custom Script Name if Desired***********************

# script_name will default to name of the directory
custom_script_name = ''

# ************************************************************************

default_directory_name = os.path.basename(os.getcwd())
script_name = custom_script_name or default_directory_name
zip_address = script_name + '.zip'


def switch_debug_to_false():

    def inplace_change(filename, old_string, new_string):
        # Safely read the input filename using 'with'
        with open(filename) as f:
            s = f.read()
            if old_string not in s:
                print("'{filename}' already set to False".format(**locals()))
                return

        # Safely write the changed content, if found in the file
        with open(filename, 'w') as f:
            print("Changing '{filename}' from {old_string} to {new_string} ".format(**locals()))
            s = s.replace(old_string, new_string)
            f.write(s)

    # check if debug file exists before trying to change boolean
    debug_file_exists = os.path.isfile('debug_mode.py')

    if debug_file_exists:
        inplace_change('debug_mode.py', 'True', 'False')
    else:
        return


def zip_files():
    z = zipfile.ZipFile(zip_address, "w")
    files_to_exclude = [zip_address, 'load_to_cs.py']
    all_files = [f for f in os.listdir('.')
                 if f not in files_to_exclude
                 and not f.endswith('.pyc')]

    for script_file in all_files:
        z.write(script_file)

    z.close()

    if zip_address in os.listdir('.'):
        print("ZIPPED UP: '{zip_address}'".format(zip_address=zip_address))
    else:
        print("ZIP FILE DOES NOT EXIST")


def load_to_cs():
    switch_debug_to_false()
    zip_files()

    ses = cs_api.CloudShellAPISession(host=server_host,
                                      username=user_name,
                                      password=password,
                                      domain=domain)

    try:
        ses.UpdateScript(script_name, zip_address)
    except Exception as e:
        print(str(e) + "\nPLEASE LOAD SCRIPT MANUALLY THE FIRST TIME")
        pass
    else:
        print(" '{script}' uploaded to CloudShell".format(script=script_name))


load_to_cs()



