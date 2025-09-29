from enum import Enum

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


############################################################
class MailForm(Enum):
    LOGIN_OTP   = "mailform/login_otp.html"
    AUTH_LINK   = "mailform/register_auth_link.html"


def send_mail(to, title, content:str) -> None:
    if not to:      raise ValueError("no_receiver_address")
    if not title:   raise ValueError("no_email_subject")
    if not content: raise ValueError("no_email_content")

    to    = to if isinstance(to, list) else [to]
    email = EmailMessage(title, content, f'"[LoopLabel]" <{settings.EMAIL_HOST_USER}>', to)
    email.content_subtype = "html"
    email.send()


def send_mail_with(to, title, form:MailForm, context:dict=None) -> None:
    content = render_to_string(form.value, context)
    send_mail(to, title, content)