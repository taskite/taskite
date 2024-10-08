from faker import Faker
import json
from django.db.models import Q
import random
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from taskite.models import Task, Board, User, TaskAssignee, TaskLabel, TaskComment


class Command(BaseCommand):
    help = "Seed tasks from a JSON file and associate them with a specific board"

    def add_arguments(self, parser):
        parser.add_argument("json_file", type=str, help="Path to the JSON file")
        parser.add_argument(
            "board_slug", type=str, help="Slug of the board to associate tasks with"
        )

    def handle(self, *args, **options):
        json_file = options["json_file"]
        board_slug = options["board_slug"]
        fake = Faker()

        try:
            # Get the board
            board = get_object_or_404(Board, slug=board_slug)
            priorities = board.priorities.all()
            states = board.states.all()
            members = (
                User.objects.filter(Q(boards=board) | Q(teams__boards=board))
                .distinct()
                .order_by("first_name")
            )
            labels = board.labels.all()

            with open(json_file, "r") as file:
                tasks_data = json.load(file)

            for task_data in tasks_data:
                task = Task.objects.create(
                    summary=task_data["summary"],
                    description=task_data["description"],
                    created_by=random.choice(members),
                    priority=random.choice(priorities),
                    state=random.choice(states),
                    board=board,
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Task {task.name} created successfully."
                    )
                )
                try:
                    random_assignee_number = random.randint(2, 6)
                    for _ in range(random_assignee_number):
                        TaskAssignee.objects.create(task=task, user=random.choice(members))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))

                try:
                    random_label_number = random.randint(2, 6)
                    for _ in range(random_label_number):
                        TaskLabel.objects.create(task=task, label=random.choice(labels))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(e))

                random_comment_number = random.randint(2, 10)
                for _ in range(random_comment_number):
                    TaskComment.objects.create(task=task, content=fake.text(), author=random.choice(members))


        except Board.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
            )
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {json_file}"))
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR(f"Invalid JSON in file: {json_file}"))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f"Missing key in JSON data: {str(e)}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
