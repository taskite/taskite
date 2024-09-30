from rest_framework import serializers

from taskite.models import Task, User


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "avatar"
        ]


class TaskSerializer(serializers.ModelSerializer):
    assignees = AssigneeSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "state_id",
            "priority_id",
            "sprint_id",
            "task_type",
            "number",
            "name",
            "summary",
            "description",
            "sequence",
            "assignees",
            "created_at",
        ]
