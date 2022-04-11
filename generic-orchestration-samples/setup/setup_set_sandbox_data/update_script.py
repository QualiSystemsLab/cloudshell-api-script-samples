"""
FLOW: - DEBUG_MODE set to False
      - directory zipped up (excluding credentials file)
      - updated on cloud-shell server
NOTE: - This script is only for updating EXISTING scripts.
      - Scripts MUST be uploaded manually first time. (this tool can still be used to do zipping)
"""

import os

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


def error_red(err_str):
    """
    for printing errors in red in pycharm.
    :param err_str:
    :return:
    """
    CRED = '\033[91m'
    CEND = '\033[0m'
    return CRED + err_str + CEND


def switch_off_debug_globals():
    import re

    def inplace_change(file_path, curr_pattern, new_string):
        with open(file_path, "r+") as f:
            text = f.read()
            pattern = re.compile(pattern=curr_pattern)
            match = pattern.search(text)
            if match:
                text = re.sub(pattern=match.group(0), repl=new_string, string=text)
                f.seek(0)
                f.write(text)
                f.truncate()

    def switch_off_global(global_var_name):
        try:
            true_string = "{} = True".format(global_var_name)
            false_string = "{} = False".format(global_var_name)
            inplace_change(file_path=debug_globals_file_path,
                           curr_pattern=true_string,
                           new_string=false_string)
        except Exception as e:
            print(error_red("[-] Issue updating {global_var} "
                            "in {debug_file}\n".format(global_var=global_var_name,
                                                       debug_file=debug_globals_file_path)
                            + str(e)))

    debug_globals_file_path = os.getcwd() + "\\" + DEBUG_GLOBALS_FILE_NAME
    debug_globals_file_exists = os.path.isfile(debug_globals_file_path)
    if debug_globals_file_exists:
        for var_name in DEBUG_GLOBAL_VARS:
            switch_off_global(var_name)
        print("[+] debug globals switched to False: {}".format(str(DEBUG_GLOBAL_VARS)))


def get_zip_details():
    parent_dir_path = os.path.abspath('.')
    parent_dir_name = os.path.basename(parent_dir_path)
    script_name = CUSTOM_SCRIPT_NAME or parent_dir_name
    zip_file_name = script_name + '.zip'

    return {"parent_dir_path": parent_dir_path,
            "parent_dir_name": parent_dir_name,
            "script_name": script_name,
            "zip_file_name": zip_file_name}


def zip_files():
    def is_whitelisted(f, file_path):
        is_regular_file = os.path.isfile(file_path)
        is_not_excluded = f not in files_to_exclude
        is_not_pyc = not f.endswith('.pyc')
        return is_regular_file and is_not_excluded and is_not_pyc

    def get_cred_file_name():
        file_name = "credentials.py"
        if EXCLUDE_CREDS_FROM_ZIP:
            return file_name
        else:
            return None

    def does_cred_file_exist():
        return os.path.isfile(get_cred_file_name())

    def get_cred_template_path():
        cred_template_file_name = "creds_template.py"
        cred_template_path = os.getcwd() + "\\" + "helper_code" + "\\" + cred_template_file_name
        return cred_template_path

    def does_cred_template_file_exist():
        template_path = get_cred_template_path()
        return os.path.isfile(template_path)

    def get_cred_template_string():
        if does_cred_template_file_exist():
            f = open(get_cred_template_path(), 'r')
            text = f.read().strip()
            f.close()
            return text

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
            # add creds template placeholder strip to zip package
            if EXCLUDE_CREDS_FROM_ZIP and does_cred_template_file_exist() and does_cred_file_exist():
                z.writestr(get_cred_file_name(), get_cred_template_string())

    zip_details = get_zip_details()
    zip_file_name = zip_details["zip_file_name"]
    dirs_to_exclude = [".git"]
    files_to_exclude = [zip_file_name, get_cred_file_name(), "venv", ".idea"]
    try:
        make_zipfile(output_filename=zip_file_name,
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
    if SWITCH_DEBUG_GLOBALS_TO_FALSE:
        switch_off_debug_globals()
    zip_files()
    cs_ses = establish_cs_session()
    zip_details = get_zip_details()
    update_script_api_wrapper(cs_ses=cs_ses,
                              script_name=zip_details["script_name"],
                              zip_address=zip_details["zip_file_name"])


update_script_on_server()
