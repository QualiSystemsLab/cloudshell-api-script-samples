"""
NOTE: - This script is only for updating EXISTING scripts.
      - Scripts MUST be uploaded manually first time. (this tool can still be used to do zipping)
"""
from cloudshell.api.cloudshell_api import CloudShellAPISession
import os

# ===== Cloudshell API Credentials ======

CLOUDSHELL_HOST = "localhost"
CLOUDSHELL_USER = "admin"
CLOUDSHELL_PASSWORD = "admin"
CLOUDSHELL_DOMAIN = "Global"

# ===== Optional Variables to set =======

# To name zip package something other than the default directory name
CUSTOM_SCRIPT_NAME = ''

# If you would like to keep your credentials bundled with zip (not recommended)
EXCLUDE_CREDS_FROM_ZIP = True

# Set to False If you don't want to switch off the debug globals
SWITCH_DEBUG_GLOBALS_TO_FALSE = True

# name of file that gets variables switched off by automation
DEBUG_GLOBALS_FILE_NAME = "DEBUG_GLOBALS.py"

# if you want to rename or add variables, must be updated here as well
DEBUG_GLOBAL_VARS = ["DEBUG_MODE"]


# =======================================


def get_api_session():
    return CloudShellAPISession(host=CLOUDSHELL_HOST,
                                username=CLOUDSHELL_USER,
                                password=CLOUDSHELL_PASSWORD,
                                domain=CLOUDSHELL_DOMAIN)


def error_red(err_str):
    """
    for printing errors in red in pycharm.
    :param err_str:
    :return:
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    return CRED + err_str + CEND


def get_zip_details():
    parent_dir_path = os.path.abspath('.')
    parent_dir_name = os.path.basename(parent_dir_path)
    script_name = CUSTOM_SCRIPT_NAME or parent_dir_name
    zip_file_name = script_name + '.zip'

    return {"parent_dir_path": parent_dir_path,
            "parent_dir_name": parent_dir_name,
            "script_name": script_name,
            "zip_file_name": zip_file_name}


def is_whitelisted(f, file_path, files_to_exclude):
    is_regular_file = os.path.isfile(file_path)
    is_not_excluded = f not in files_to_exclude
    is_not_pyc = not f.endswith('.pyc')
    return is_regular_file and is_not_excluded and is_not_pyc


def make_zipfile(output_filename, source_dir, files_to_exclude, dirs_to_exclude):
    import zipfile
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(source_dir):
            dirs[:] = [d for d in dirs if d not in dirs_to_exclude]
            for f in files:
                file_path = os.path.join(root, f)
                if is_whitelisted(f, file_path, files_to_exclude):
                    arcname = os.path.join(os.path.relpath(root, source_dir), f)
                    z.write(file_path, arcname)


def zip_files():
    zip_details = get_zip_details()
    zip_file_name = zip_details["zip_file_name"]
    dirs_to_exclude = [".git"]
    files_to_exclude = [zip_file_name, "venv", ".idea", "update_script.py", "DEBUG.py"]
    try:
        make_zipfile(output_filename=zip_file_name,
                     source_dir=zip_details["parent_dir_path"],
                     files_to_exclude=files_to_exclude,
                     dirs_to_exclude=dirs_to_exclude)
    except Exception as e:
        print(error_red("[-] error zipping up file: " + str(e)))
        exit(1)
    else:
        if zip_file_name in os.listdir("."):
            print("[+] ZIPPED UP: '{zip_name}'".format(zip_name=zip_file_name))
        else:
            print("[-] ZIP FILE NOT PRESENT")


def update_script_api_wrapper(cs_ses, script_name, zip_address):
    try:
        cs_ses.UpdateScript(script_name, zip_address)
    except Exception as e:
        print(error_red("[-] ERROR UPDATING SCRIPT IN PORTAL\n" + str(e)) + "\n"
                                                                            "PLEASE LOAD SCRIPT MANUALLY THE FIRST TIME")
        exit(1)
    else:
        print("[+] '{script}' updated on CloudShell Successfully".format(script=script_name))


def update_script_on_server():
    zip_files()
    cs_ses = get_api_session()
    zip_details = get_zip_details()
    update_script_api_wrapper(cs_ses=cs_ses,
                              script_name=zip_details["script_name"],
                              zip_address=zip_details["zip_file_name"])


update_script_on_server()
