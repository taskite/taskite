from faker import Faker
import random
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from taskite.models import Task, Board, User, TaskAssignee, TaskLabel, TaskComment
from taskite.management.commands.sample_tasks import tasks as sample_tasks


class Command(BaseCommand):
    help = "Seed tasks for a specific board"

    def add_arguments(self, parser):
        parser.add_argument(
            "board_slug", type=str, help="Slug of the board to associate tasks with"
        )

    def create_tasks(
        self, board, priorities, labels, states, members, task_data, parent=None
    ):
        task = Task.objects.create(
            summary=task_data["summary"],
            description=task_data["description"],
            created_by=random.choice(members),
            priority=random.choice(priorities),
            state=random.choice(states),
            board=board,
            parent=parent,
        )

        self.stdout.write(self.style.SUCCESS(f"Task {task.name} created successfully."))
        try:
            for _ in range(task_data["assignee_count"] + 1):
                TaskAssignee.objects.create(task=task, user=random.choice(members))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

        try:
            for _ in range(task_data["labels_count"] + 1):
                TaskLabel.objects.create(task=task, label=random.choice(labels))
        except Exception as e:
            self.stdout.write(self.style.ERROR(e))

        for comment in task_data["comments"]:
            TaskComment.objects.create(
                task=task,
                content=comment,
                author=random.choice(members),
                comment_type=TaskComment.CommentType.UPDATE
            )

        if "subtasks" in task_data:
            for subtask_data in task_data["subtasks"]:
                print(subtask_data)
                self.create_tasks(
                    board, priorities, labels, states, members, subtask_data, task
                )

    def handle(self, *args, **options):
        board_slug = options["board_slug"]
        board = get_object_or_404(Board, slug=board_slug)
        priorities = board.priorities.all()
        states = board.states.all()
        members = (
            User.objects.filter(user_board_permissions__board=board)
            .distinct()
            .order_by("first_name")
        )
        labels = board.labels.all()
        try:
            for task_data in sample_tasks:
                self.create_tasks(
                    board, priorities, labels, states, members, task_data, None
                )

        except Board.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
            )
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing key in JSON data: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
