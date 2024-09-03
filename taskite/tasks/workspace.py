from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from celery import shared_task

from taskite.models.workspace import WorkspaceInvite


@shared_task
def workspace_invite_confirm(invite_id):
    invite = WorkspaceInvite.objects.filter(id=invite_id).first()
    html_content = render_to_string(
        "emails/workspaces/invite_confirm.html", {"invite": invite}
    )
    text_content = strip_tags(html_content)
    try:
        send_mail(
            subject="Workspace Invite",
            message=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[invite.email],
            html_message=html_content,
            fail_silently=False,
        )
        print('success')
    except Exception as e:
        print(e)

