from django.core.mail import send_mail
from Insportify import settings

def email(sub, msg, recipients):
    send_mail( sub, msg, settings.EMAIL_HOST_USER, recipients )
    return True
