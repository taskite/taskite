# Generated by Django 5.1 on 2024-12-05 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0050_taskattachment_filename"),
    ]

    operations = [
        migrations.AddField(
            model_name="taskattachment",
            name="mime_type",
            field=models.CharField(default="image/png", max_length=50),
            preserve_default=False,
        ),
    ]
