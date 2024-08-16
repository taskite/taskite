from django.db.models.signals import post_save
from django.dispatch import receiver

from taskite.models import OrganizationUser, Organization


@receiver(post_save, sender=Organization)
def create_organization_owner(sender, instance, created, **kwargs):
    if created:
        OrganizationUser.objects.create(
            organization=instance,
            user=instance.created_by,
            role=OrganizationUser.Role.OWNER,
        )
