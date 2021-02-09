"""
FLOW: - DEBUG_PRINT set to False
      - directory zipped up (excluding credentials file)
      - updated on cloud-shell server
NOTE: - This script is only for updating EXISTING scripts.
      - Scripts MUST be uploaded manually first time. (this tool can still be used to do zipping)
"""

import os


# ===== Optional Variables to set =======

# To name script something other than the default directory name
CUSTOM_SCRIPT_NAME = ''

# If you would like to keep your credentials bundled with zip (not recommended)
EXCLUDE_CREDS_FROM_ZIP = True
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


def switch_off_debug_print():
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

    debug_print_file_name = "DEBUG_PRINT.py"
    debug_print_file_path = os.getcwd() + "\\" + debug_print_file_name
    debug_print_file_exists = os.path.isfile(debug_print_file_path)
    if debug_print_file_exists:
        try:
            inplace_change(filename=debug_print_file_path,
                           curr_pattern="DEBUG_PRINT = True",
                           new_string="DEBUG_PRINT = False")
        except Exception as e:
            print(error_red("[-] Issue updating {debug_file}\n".format(debug_file=debug_print_file_path)
                            + str(e)))
        else:
            print('[+] DEBUG_PRINT set to False before zipping')


def get_zip_details():
    parent_dir_path = os.path.abspath('.')
    parent_dir_name = os.path.basename(parent_dir_path)
    zip_file_name = parent_dir_name + '.zip'

    return {"parent_dir_path": parent_dir_path,
            "parent_dir_name": parent_dir_name,
            "zip_file_name": zip_file_name}


def zip_files():
    if EXCLUDE_CREDS_FROM_ZIP:
        cred_file = "credentials.py"
    else:
        cred_file = ""

    zip_details = get_zip_details()
    zip_file_name = zip_details["zip_file_name"]
    dirs_to_exclude = [".git", "dist"]
    files_to_exclude = [zip_file_name, cred_file, "venv", ".idea"]

    def is_whitelisted(f, file_path):
        is_regular_file = os.path.isfile(file_path)
        is_not_excluded = f not in files_to_exclude
        is_not_pyc = not f.endswith('.pyc')
        return is_regular_file and is_not_excluded and is_not_pyc

    def get_cred_template_string():
        template_path = "helper_code\\creds_template.py"
        f = open(template_path, 'r')
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
            # add dummy creds file to zip package
            if EXCLUDE_CREDS_FROM_ZIP:
                z.writestr("credentials.py", get_cred_template_string())

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
    switch_off_debug_print()
    zip_files()
    zip_details = get_zip_details()
    script_name = CUSTOM_SCRIPT_NAME or zip_details["parent_dir_name"]
    cs_ses = establish_cs_session()
    update_script_api_wrapper(cs_ses=cs_ses,
                              script_name=script_name,
                              zip_address=zip_details["zip_file_name"])


update_script_on_server()



