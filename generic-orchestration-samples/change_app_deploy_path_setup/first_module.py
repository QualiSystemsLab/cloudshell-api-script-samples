from cloudshell.workflow.orchestration.sandbox import Sandbox
from custom_helpers import sb_print
from custom_helpers import get_sandbox_apps
from cloudshell.api.cloudshell_api import *
from debug_mode import debug_mode

# global list for tracking app names that have a request set so they can be skipped over
apps_set_memory = []

# global list that stores the app edit requests passed to the API call
app_edit_requests = []


def construct_deployment(sandbox, curr_app, desired_deployment):
    attrib_list = [NameValuePair(att.Name, att.Value) for att in desired_deployment.DeploymentService.Attributes]
    new_deployment = DefaultDeployment(desired_deployment.Name, Deployment(attrib_list))
    app_edit_requests.append(ApiEditAppRequest(Name=curr_app.Name,
                                               NewName=curr_app.Name,
                                               Description=curr_app.Description,
                                               AppDetails=None,
                                               DefaultDeployment=new_deployment))
    apps_set_memory.append(curr_app.Name)
    sb_print(sandbox, "{app_name} deployment request: {dp_name}".format(app_name=curr_app.Name,
                                                                        dp_name=desired_deployment.Name))


def set_app_edit_requests(sandbox, requested_deployment_names):
    sandbox_apps = get_sandbox_apps(sandbox)
    match_counter = 0
    for curr_app in sandbox_apps:
        # if match is found, move to next app
        if match_counter > 0:
            break

        # skip over apps with request already set
        if curr_app.Name in apps_set_memory:
            continue

        matching_deployment = [deployment for deployment in curr_app.DeploymentPaths
                               if deployment.Name in requested_deployment_names]

        if matching_deployment:
            desired_deployment = matching_deployment[0]
            match_counter = 1
            construct_deployment(sandbox, curr_app, desired_deployment)


def set_requested_deployment_paths(sandbox, requested_deployment_names):
    for deployment_name in requested_deployment_names:
        set_app_edit_requests(sandbox, deployment_name)

    app_edit_requests_len = len(app_edit_requests)
    requested_dep_names_len = len(requested_deployment_names)

    # If these match then all the requested apps have a corresponding request to be sent to API
    if app_edit_requests_len == requested_dep_names_len:
        try:
            sandbox.automation_api.EditAppsInReservation(sandbox.id, app_edit_requests)
        except Exception as e:
            sb_print(sandbox, "there was an error with the app edits request: " + str(e))
        else:
            sb_print(sandbox, "=== app edit requests successfully sent ===")
    else:
        sb_print(sandbox, "=== There was an issue setting one of the app deployment paths ===\n"
                          "=== Please confirm that user inputs and deployment paths match ===")


# ========== Primary Function ==========
def run_custom_setup(sandbox, components):
    """
    :param Sandbox sandbox:
    :param components
    :return:
    """
    global_inputs = sandbox.global_inputs
    global_inputs_str = str(global_inputs)

    if debug_mode:
        # sb_print(sandbox, "sandbox inputs: " + global_inputs_str)
        pass

    if debug_mode:
        requested_deployment_names = ["default(2gb ram)", "medium(4gb ram)", "large(8gb ram)"]
    else:
        requested_deployment_names = [value for key, value in global_inputs.iteritems()
                                      if key.startswith("vm #")]

    requested_dep_names_str = str(requested_deployment_names)
    sb_print(sandbox, "requested inputs: " + requested_dep_names_str)
    sb_print(sandbox, "===============================")

    set_requested_deployment_paths(sandbox, requested_deployment_names)
    pass

