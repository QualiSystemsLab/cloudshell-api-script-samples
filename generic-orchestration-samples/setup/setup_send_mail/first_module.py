import os

from cloudshell.api.cloudshell_api import InputNameValue
from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.sandbox_print_helpers import *
import helper_code.automation_api_helpers as api_help
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as script_help
from sb_rest.sandbox_rest_api import SandboxRest
from setup_ended_html_template import get_email_template

PORTAL_URL = "http://10.212.128.6:3001"
EMAIL_TEMPLATE = "training_portal_alert.html"
SMTP_RESOURCE = "Admin SMTP"


# ========== Primary Function ==========
def first_module_flow(sandbox, components=None):
    """
    Functions passed into orchestration flow MUST have (sandbox, components) signature
    :param Sandbox sandbox:
    :param components
    :return:
    """
    api = sandbox.automation_api
    res_id = sandbox.id
    res_details = api.GetReservationDetails(res_id, True).ReservationDescription
    resources = res_details.Resources
    root_resources = [x for x in resources if "/" not in x.Name]
    sandbox_owner = res_details.Owner
    owner_email = api.GetUserDetails(sandbox_owner).Email
    current_time = api.GetServerDateAndTime()
    start_time = res_details.StartTime
    end_time = res_details.EndTime

    sb_rest = SandboxRest(server=sandbox.connectivityContextDetails.server_address,
                          username=sandbox.connectivityContextDetails.admin_user,
                          password=sandbox.connectivityContextDetails.admin_pass,
                          domain=sandbox.reservationContextDetails.DOMAIN)

    token = sb_rest.get_user_token(sandbox.reservationContextDetails.owner_user)

    portal_link = "{}/{}?access={}".format(PORTAL_URL, sandbox.id, token)

    # current_dir = os.path.abspath(os.path.dirname(__file__))
    # template_path = os.path.join(current_dir, EMAIL_TEMPLATE)
    #
    # with open(template_path) as template_file:
    #     file_data = template_file.read()
    #     formatted_html = file_data.format(user=sandbox_owner,
    #                                       sandbox_name=sandbox.reservationContextDetails.environment_name,
    #                                       link=portal_link)
    # email_body = """
    #         <h2>Hello {user}, your training portal is ready.</h2>
    #         <a href="{link}">here</a>
    #         """.format(user=sandbox_owner, link=portal_link)

    email_body = get_email_template(sb_name=res_details.Name,
                                    res_id=res_id,
                                    current_time=current_time,
                                    training_portal_link=portal_link,
                                    sb_owner=sandbox_owner,
                                    start_time=start_time,
                                    end_time=end_time,
                                    sb_description=res_details.Description,
                                    resource_count=len(root_resources),
                                    blueprint_name=res_details.Topologies[0])

    # sending mail
    mail_inputs = [
        InputNameValue("message_title", "Hello '{}', your training portal is ready.".format(sandbox_owner)),
        InputNameValue("message_body", email_body),
        InputNameValue("recipients", owner_email),
        InputNameValue("cc_recipients", "")
    ]
    warn_print(api, res_id, "Sending training portal mail to user...")
    try:
        mail_response = api.ExecuteCommand(reservationId=res_id,
                                           targetName=SMTP_RESOURCE,
                                           targetType="Resource",
                                           commandName="send_mail",
                                           commandInputs=mail_inputs)
    except Exception as e:
        err_print(api, res_id, "=== Issue sending mail ===")
        err_print(api, res_id, str(e))
        info = "Issue sending mail. Check '{}' SMTP Resource. Error: {}".format(SMTP_RESOURCE, str(e))
        api.SetReservationLiveStatus(reservationId=res_id,
                                     liveStatusName="Error",
                                     additionalInfo=info)
        raise
    else:
        sb_print(api, res_id, mail_response.Output)
