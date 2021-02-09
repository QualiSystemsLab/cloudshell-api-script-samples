from cloudshell.api.cloudshell_api import CloudShellAPISession
from datetime import datetime, timedelta
import time

# format is "days.hours:minutes:seconds, similar to how automation api returns max duration time"
# Leave Zero padding on each unit or script will break
TARGET_MAX_DURATION_STR = '00.02:00:00'

# api session details
user = "admin"
password = "admin"
server = "localhost"
domain = "Global"

api = CloudShellAPISession(host=server, username=user, password=password, domain=domain)


def get_seconds_from_date_string(date_string):
    """
    sample date string - '01.01:02:00'; 'Days.Hours:Minutes:Seconds'
    Days portion will not appear if max reservation is less than a day
    :param str date_string:
    :return:
    """
    if "." in date_string:
        split_str = date_string.split(".")
        days = int(split_str[0])
        hours_min_sec_str = split_str[1]
        seconds_from_days = days * 24 * 60 * 60
    else:
        hours_min_sec_str = date_string
        seconds_from_days = 0

    duration_dt = time.strptime(hours_min_sec_str, "%H:%M:%S")
    seconds_from_time_str = timedelta(hours=duration_dt.tm_hour,
                                      minutes=duration_dt.tm_min,
                                      seconds=duration_dt.tm_sec).total_seconds()

    total_seconds = seconds_from_days + seconds_from_time_str
    return total_seconds


def is_max_duration_less_than_target(api, blueprint_name):
    """
    search current blueprint resources for presence of the Target Resource
    :param CloudShellAPISession api:
    :param str blueprint_name:
    :param [str] target_res_names:
    :return:
    """
    details = api.GetTopologyDetails(blueprint_name)
    max_duration_str = details.MaxDuration

    # If there is no max duration set, it will be a None object
    if not max_duration_str:
        return True

    max_duration_seconds = get_seconds_from_date_string(max_duration_str)
    target_duration_seconds = get_seconds_from_date_string(TARGET_MAX_DURATION_STR)
    if max_duration_seconds >= target_duration_seconds:
        return True
    else:
        return False


def get_blueprint_data(api, blueprint_name):
    details = api.GetTopologyDetails(blueprint_name)
    bp_owner = details.Owner
    max_duration = details.MaxDuration
    return blueprint_name, bp_owner, max_duration


all_blueprints = api.GetTopologiesByCategory().Topologies
target_blueprints = [bp_name for bp_name in all_blueprints
                     if is_max_duration_less_than_target(api, bp_name)]

target_bp_data = [get_blueprint_data(api, bp_name) for bp_name in target_blueprints]

# add blueprint report to text file
report_file_name = 'target_blueprints.txt'

print("=== Target Blueprints exceeding Target Max Duration of '{}'===".format(TARGET_MAX_DURATION_STR))
with open(report_file_name, 'w') as f:
    header_row = "\t{0:<50} {1:<50} {2}".format("BLUEPRINT", "OWNER", "DURATION")
    print(header_row)
    print >> f, header_row
    for index, bp_data in enumerate(target_bp_data):
        row = "{}. {:<50} {:<50} {}".format(str(index), bp_data[0], bp_data[1], bp_data[2])
        print row
        print >> f, row

print("\n===========")
print("blueprints logged to report file '{}'".format(report_file_name))
