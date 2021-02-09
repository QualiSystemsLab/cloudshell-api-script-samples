"""
FLOW: debug_mode.py set to False > script is zipped up > updated in Cloudshell portal.
NOTE: This script is only for updating EXISTING scripts in Cloudshell portal.
      Zip must be uploaded manually first time in MANAGE > SCRIPTS.
WARNING: This script will update and overwrite existing scripts with same name.
"""

import os
from dev_utility import error_red


# ===== Optional Variables to set =======

# TO NAME ZIP FOLDER SOMETHING OTHER THAN MAIN DIRECTORY NAME
CUSTOM_SCRIPT_NAME = ''

# TO EXCLUDE THE USER CREDENTIALS FILE FROM GENERATED ZIP FOLDER
EXCLUDE_CREDS_FROM_ZIP = False

# =======================================


def switch_debug_to_false():
    import re

    def inplace_change(filename, curr_pattern, new_string):
        with open(filename, "r+") as f:
            text = f.read()
            pattern = re.compile(pattern=curr_pattern)
            match = pattern.search(text)
            if match:
                text = re.sub(pattern=match.group(0), repl=new_string, string=text)
                f.seek(0)
                f.write(text)
                f.truncate()

    BASE_DIR = os.path.dirname(os.getcwd())
    debug_file = BASE_DIR + "\\" + "control_flow.py"
    debug_file_exists = os.path.isfile(debug_file)
    if debug_file_exists:
        try:
            inplace_change(filename=debug_file,
                           curr_pattern="DEBUG_MODE = True",
                           new_string="DEBUG_MODE = False")
        except Exception as e:
            print(error_red("[-] Issue updating {debug_file}\n".format(debug_file=debug_file)
                            + str(e)))
        else:
            print('[+] DEBUG_MODE set to False before zipping')


def get_zip_details():
    parent_dir_path = os.path.abspath('..')
    parent_dir_name = os.path.basename(parent_dir_path)
    zip_file_name = parent_dir_name + '.zip'

    return {"parent_dir_path": parent_dir_path,
            "parent_dir_name": parent_dir_name,
            "zip_file_name": zip_file_name}


def zip_files():
    zip_details = get_zip_details()
    zip_file_name = zip_details["zip_file_name"]
    dirs_to_exclude = [".git", "dist"]
    if EXCLUDE_CREDS_FROM_ZIP:
        creds = "credentials.py"
    else:
        creds = ''
    files_to_exclude = [zip_file_name, creds, "venv", ".idea"]

    def is_whitelisted(f, file_path):
        is_regular_file = os.path.isfile(file_path)
        is_not_excluded = f not in files_to_exclude
        is_not_pyc = not f.endswith('.pyc')
        return is_regular_file and is_not_excluded and is_not_pyc

    def make_zipfile(output_filename, source_dir):
        import zipfile
        with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(source_dir):
                dirs[:] = [d for d in dirs if d not in dirs_to_exclude]
                for f in files:
                    file_path = os.path.join(root, f)
                    if is_whitelisted(f, file_path):
                        arcname = os.path.join(os.path.relpath(root, source_dir), f)
                        z.write(file_path, arcname)

    try:
        make_zipfile(output_filename=zip_details["zip_file_name"],
                     source_dir=zip_details["parent_dir_path"])
    except Exception as e:
        print(error_red("[-] error zipping up file: " + str(e)))
        exit(1)
    else:
        if zip_file_name in os.listdir("."):
            print("[+] ZIPPED UP: '{zip_name}'".format(zip_name=zip_file_name))
        else:
            print("[-] ZIP FILE NOT PRESENT")


def establish_cs_session():
    from credentials import credentials
    import cloudshell.api.cloudshell_api as cs_api
    try:
        ses = cs_api.CloudShellAPISession(host=credentials["server"],
                                          username=credentials["user"],
                                          password=credentials["password"],
                                          domain=credentials["domain"])
    except Exception as e:
        print(error_red("[-] ERROR ESTABLISHING CS_API SESSION. CHECK CREDENTIALS AND CONNECTIVITY.\n" + str(e)))
        exit(1)
    else:
        return ses


def update_script(cs_ses, script_name, zip_address):
    try:
        cs_ses.UpdateScript(script_name, zip_address)
    except Exception as e:
        print(error_red("[-] ERROR UPDATING SCRIPT IN PORTAL\n" + str(e)) + "\n"
              "PLEASE LOAD SCRIPT MANUALLY THE FIRST TIME")
        exit(1)
    else:
        print("[+] '{script}' updated on CloudShell Successfully".format(script=script_name))


def load_to_cs():
    switch_debug_to_false()
    zip_files()
    zip_details = get_zip_details()
    script_name = CUSTOM_SCRIPT_NAME or zip_details["parent_dir_name"]
    cs_ses = establish_cs_session()
    update_script(cs_ses=cs_ses,
                  script_name=script_name,
                  zip_address=zip_details["zip_file_name"])


load_to_cs()



