# Generated by Django 5.1 on 2024-12-05 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0051_taskattachment_mime_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="taskattachment",
            name="mime_type",
            field=models.CharField(max_length=121),
        ),
    ]