# Generated by Django 5.1 on 2024-10-06 14:38

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("taskite", "0019_label"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskLabel",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "label",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="label_task_labels",
                        to="taskite.label",
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="task_labels",
                        to="taskite.task",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task Label",
                "verbose_name_plural": "Task Labels",
                "db_table": "task_labels",
            },
        ),
    ]