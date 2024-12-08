# Generated by Django 5.1 on 2024-10-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0045_alter_boardpermission_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="boardteampermission",
            name="role",
            field=models.CharField(
                choices=[
                    ("admin", "Admin"),
                    ("collaborator", "Collaborator"),
                    ("maintainer", "Maintainer"),
                    ("guest", "Guest"),
                ],
                default="collaborator",
                max_length=20,
            ),
        ),
    ]
