# Generated by Django 5.1 on 2024-09-22 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0006_team_avatar"),
    ]

    operations = [
        migrations.AddField(
            model_name="workspaceinvite",
            name="accepted_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]