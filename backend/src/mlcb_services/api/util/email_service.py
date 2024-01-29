import logging
import os
import smtplib
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EMAIL SERVICE LOGGING")


def send_email(to_email: str, template: str, **kwargs):
    msg = MIMEText(template.format(**kwargs))
    msg['Subject'] = kwargs['subject']
    msg['From'] = os.getenv("EMAIL_SERVICE_ACCOUNT")
    msg['To'] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as email_server:
            email_server.starttls()
            email_server.login(os.getenv("GOOGLE_ACCOUNT"), os.getenv("GOOGLE_APP_PASS"))
            email_server.send_message(msg)
            logger.info("Confirmation Email sent successfully!")
    except smtplib.SMTPException as error:
        logger.error(f"Error sending email: {error}")
