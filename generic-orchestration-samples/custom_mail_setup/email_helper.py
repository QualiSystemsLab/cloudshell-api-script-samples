import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(smtp_user, smtp_pass, smtp_address, smtp_port, recipients, message_title, message_body, is_html):
    try:
        recipient_list = str.split(recipients, ',')

        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = message_title
        msg['From'] = smtp_user
        msg['To'] = recipient_list[0]
        if len(recipient_list) > 1: msg['Cc'] = ', '.join(recipient_list[1:])

        # Create the body of the message (a plain-text and an HTML version).
        if is_html:
            text = message_body
            html = message_body
        else:
            text = message_body
            html = None
        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)

        # Send the message via local SMTP server.
        smtp_session = smtplib.SMTP(smtp_address, smtp_port)
        smtp_session.ehlo()
        smtp_session.starttls()
        if smtp_user:
            login_res = smtp_session.login(smtp_user, smtp_pass)

        # sendmail function takes 3 arguments: sender's address, recipient's address
        # and message to send - here it is sent as one string.
        smtp_session.sendmail(smtp_user, recipient_list, msg.as_string())
        smtp_session.quit()
        return True
    except Exception:
        return False
