# Generated by Django 5.1 on 2024-12-18 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0061_sprint_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="is_template",
            field=models.BooleanField(default=False),
        ),
    ]
