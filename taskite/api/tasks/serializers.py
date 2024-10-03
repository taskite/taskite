from rest_framework import serializers

from taskite.models import Task, User, Priority


class AssigneeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "avatar"]


class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "avatar"]


class QuerySerializer(serializers.Serializer):
    assignees = serializers.ListField(child=serializers.UUIDField(), required=False)


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ["id", "name", "created_at"]


class TaskCreateSerializer(serializers.Serializer):
    summary = serializers.CharField()
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    task_type = serializers.ChoiceField(choices=Task.TaskType.choices)
    state_id = serializers.UUIDField()
    priority_id = serializers.UUIDField(required=False, allow_null=True)
    assignees = serializers.ListField(child=serializers.UUIDField(), required=False, allow_empty=True)


class TaskSerializer(serializers.ModelSerializer):
    assignees = AssigneeSerializer(many=True)
    priority = PrioritySerializer()
    created_by = CreatedBySerializer()

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
            "priority",
            "created_by",
            "created_at",
        ]


class TaskSequenceUpdateSerializer(serializers.Serializer):
    previous_task = serializers.UUIDField(required=False)
    state_id = serializers.UUIDField()
    next_task = serializers.UUIDField(required=False)
