"""
This script zips up all files into an archive and then updates script on cloudshell server
Usage:
- Populate cloudshell api credentials
- Run this script from inside the target script directory, otherwise pass the full path as argument if running from elsewhere
- A custom script name can be passed, otherwise falls back to current directory name

Notes:
- Zip will be generated into a dist folder, and will exclude all unneccesary files
- This script supports zipping up scripts with nested folders / modules
- Will throw validation error if __main__.py is not found
"""
import sys
import zipfile
from dataclasses import dataclass
from typing import List

from cloudshell.api.cloudshell_api import CloudShellAPISession, CloudShellAPIError
import os
from pathlib import Path

DIRS_TO_EXCLUDE = [".git", "dist", "venv", ".idea", ".lol"]
FILES_TO_EXCLUDE = ["credentials.py"]


def error_red(err_str):
    cred = '\033[91m'
    cend = '\033[0m'
    return cred + err_str + cend


@dataclass
class ZipDetails:
    script_dir_path: str
    script_dir_name: str
    script_name: str
    zip_file_name: str
    archive_path: str


def _get_zip_details(script_dir_path: str, script_name: str):
    zip_file_name = script_name + '.zip'
    archive_path = os.path.join(script_dir_path, "dist", zip_file_name)
    return ZipDetails(script_dir_path=script_dir_path,
                      script_dir_name=os.path.basename(script_dir_path),
                      script_name=script_name,
                      zip_file_name=f"{script_name}.zip",
                      archive_path=archive_path)


def _is_valid_file(file_name: str, file_path: str, files_to_exclude: List[str]):
    invalid_conditions = [file_name.endswith(".pyc"),
                          file_name.endswith(".zip"),
                          file_name in files_to_exclude,
                          file_name == os.path.basename(__file__),  # exclude the updater script
                          not os.path.isfile(file_path)]
    if any(invalid_conditions):
        return False
    return True


def _create_zip_archive(archive_path: str, src_path: str):
    with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive_file:
        for dirpath, dirnames, filenames in os.walk(src_path):
            dir_name = os.path.basename(dirpath)

            # validate top level folder that it has a __main__.py entry point
            if dir_name == os.path.basename(src_path) and "__main__.py" not in filenames:
                print(error_red(f"No '__main__.py' file found in '{dir_name}' Directory. Not a valid cloudshell script."))
                sys.exit(1)

            # skip dist and other excluded folders
            if dir_name in DIRS_TO_EXCLUDE:
                continue

            # validate files and add to archive
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if not _is_valid_file(filename, file_path, FILES_TO_EXCLUDE):
                    continue
                archive_file_path = os.path.relpath(file_path, src_path)
                archive_file.write(file_path, archive_file_path)

    # validate generated zip archive
    with zipfile.ZipFile(archive_path, 'r') as archive_file:
        bad_file = zipfile.ZipFile.testzip(archive_file)

        if bad_file:
            raise zipfile.BadZipFile('CRC check failed for {} with file {}'.format(archive_path, bad_file))


def _zip_files(zip_details: ZipDetails):
    try:
        _create_zip_archive(archive_path=zip_details.archive_path, src_path=zip_details.script_dir_path)
    except Exception as e:
        err_msg = f"Error zipping up file: {type(e).__name__}: {str(e)}"
        raise Exception(err_msg)


def _update_script(api: CloudShellAPISession, script_name: str, zip_name: str):
    try:
        api.UpdateScript(script_name, zip_name)
    except CloudShellAPIError as e:
        if e.code == "100":
            err_msg = f"[-] '{script_name}' update FAILED. {str(e)}. (Please upload manually first time)."
            print(error_red(err_msg))
            sys.exit(1)
        raise


def _create_dist_folder(script_dir_path: str):
    Path(f"{script_dir_path}/dist").mkdir(exist_ok=True)


def update_script_on_server(api: CloudShellAPISession, script_name: str = None, script_dir_path: str = None):
    script_dir_path = script_dir_path or os.path.abspath('.')
    script_name = script_name or os.path.basename(script_dir_path)

    _create_dist_folder(script_dir_path)
    zip_details = _get_zip_details(script_dir_path, script_name)
    _zip_files(zip_details)
    print(" [+] ZIPPED UP: '{zip_name}'".format(zip_name=zip_details.zip_file_name))
    _update_script(api, script_name=zip_details.script_name, zip_name=zip_details.archive_path)
    print(f"[+] '{script_name}' updated on CloudShell Successfully")


if __name__ == "__main__":
    cs_api = CloudShellAPISession("localhost", "admin", "admin", "Global")
    update_script_on_server(cs_api)
