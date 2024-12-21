from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task
from sentry_sdk import capture_exception

from calyvim.models.user import User

@shared_task
def send_welcome_email(email_address):
    user = User.objects.filter(email=email_address).first()
    html_content = render_to_string("accounts/home/welcome.html", {"user": user})
    text_content = strip_tags(html_content)

    try:
        send_mail(
            subject="Welcome to calyvim",
            message=text_content,
            from_email=settings.DEFAULT_EMAIL,
            recipient_list=[user.email],
            html_message=html_content,
            fail_silently=False,
        )
    except Exception as e:
        capture_exception(e)