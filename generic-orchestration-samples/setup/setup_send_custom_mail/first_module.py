from cloudshell.workflow.orchestration.sandbox import Sandbox
from helper_code.custom_helpers import sb_print
from email_helper import send_email


def send_email_to_owner(sandbox):
    """
    :param sandbox:
    :param components:
    :type sandbox Sandbox
    :return:
    """
    user_details = sandbox.automation_api.GetUserDetails(sandbox.reservationContextDetails.owner_user)
    if user_details.Email == '':
        return

    SMTP_resource = sandbox.automation_api.FindResources('Mail Server', 'SMTP Server').Resources[0]
    SMTP_resource_details = sandbox.automation_api.GetResourceDetails(SMTP_resource.FullPath)
    SMTP_atts = {att.Name: att.Value for att in SMTP_resource_details.ResourceAttributes if att.Type != "Password"}
    SMTP_atts.update({att.Name: sandbox.automation_api.DecryptPassword(att.Value).Value for att in
                      SMTP_resource_details.ResourceAttributes if att.Type == "Password"})

    sandbox_details = sandbox.automation_api.GetReservationDetails(sandbox.id).ReservationDescription
    email_title = "Setup for Sandbox: '{}' completed successfully".format(sandbox_details.Name)
    reservation_resource_details = ""
    for resource in sandbox_details.Resources:
        if resource.ResourceFamilyName == "Generic App Family":
            resource_attributes_dict = {att.Name: att.Value for att in
                                        sandbox.automation_api.GetResourceDetails(resource.Name).ResourceAttributes}

            decrypted_resource_pw = sandbox.automation_api.DecryptPassword(
                encryptedString=resource_attributes_dict["Password"]).Value

            reservation_resource_details += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td></tr>".format(
                resource.Name,
                resource.FullAddress,
                resource_attributes_dict["User"],
                decrypted_resource_pw)

    template_file_path = 'C:\\Quali_Files\\Email_Templates\\SetupCompleteEmailTemplate.html'
    message_body = open(template_file_path).read().format(
        sandbox_details.Name, sandbox_details.Owner, sandbox.id, sandbox_details.Description,
        sandbox_details.Topologies[0], reservation_resource_details)
    email_res = send_email(smtp_user=SMTP_atts["User"],
                           smtp_pass=SMTP_atts["Password"],
                           smtp_address=SMTP_resource_details.Address,
                           smtp_port=SMTP_atts["Port"],
                           recipients=user_details.Email,
                           message_title=email_title,
                           message_body=message_body,
                           is_html=True)
    pass


# ========== Primary Function ==========
def first_module_flow(sandbox, components):
    """
    :param Sandbox sandbox:
    :param components
    :return:
    """

    send_email_to_owner(sandbox)

