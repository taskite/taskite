from faker import Faker
import random
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
import math
from calyvim.models import (
    Task,
    Board,
    User,
    TaskAssignee,
    TaskLabel,
    TaskComment,
    Sprint,
)
from calyvim.management.commands.sample_tasks import tasks as sample_tasks
from calyvim.management.commands.tasks.sprint_1 import tasks as sprint_1_tasks
from calyvim.management.commands.tasks.sprint_2 import tasks as sprint_2_tasks
from calyvim.management.commands.tasks.sprint_3 import tasks as sprint_3_tasks
from calyvim.management.commands.tasks.sprint_4 import tasks as sprint_4_tasks
from calyvim.management.commands.tasks.sprint_5 import tasks as sprint_5_tasks


def get_quarter(date):
    return math.ceil(date.month / 3)


# Calculate base dates
current_date = timezone.now().date()
sprint_duration = timedelta(days=14)
oldest_start = current_date - (sprint_duration * 5)


def get_quarter(date):
    return math.ceil(date.month / 3)


def get_sprint_number_in_quarter(date):
    # Get the first day of the quarter
    quarter_start_month = (get_quarter(date) - 1) * 3 + 1
    quarter_start = date.replace(month=quarter_start_month, day=1)

    # Calculate days since quarter start
    days_since_quarter_start = (date - quarter_start).days

    # Calculate sprint number (1-based index)
    return math.ceil((days_since_quarter_start + 1) / 14)


class Command(BaseCommand):
    help = "Seed tasks for a specific board"

    def add_arguments(self, parser):
        parser.add_argument(
            "board_slug", type=str, help="Slug of the board to associate tasks with"
        )

    def create_tasks(
        self,
        board,
        priorities,
        labels,
        states,
        members,
        estimates,
        task_data,
        sprint=None,
        parent=None,
    ):
        task = Task.objects.create(
            summary=task_data["summary"],
            description=task_data["description"],
            created_by=random.choice(members),
            priority=random.choice(priorities),
            state=random.choice(states),
            estimate=random.choice(estimates),
            board=board,
            sprint=sprint,
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
                comment_type=TaskComment.CommentType.UPDATE,
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
        estimates = board.estimates.all()
        members = (
            User.objects.filter(user_board_permissions__board=board)
            .distinct()
            .order_by("first_name")
        )
        labels = board.labels.all()

        # Calculate base dates
        current_date = timezone.now().date()
        sprint_duration = timedelta(days=14)
        oldest_start = current_date - (sprint_duration * 5)

        # Sprint 1 (Oldest)
        sprint1_start = oldest_start
        sprint1_end = sprint1_start + sprint_duration
        sprint1_name = f"Sprint {sprint1_start.year}.Q{get_quarter(sprint1_start)}.{get_sprint_number_in_quarter(sprint1_start)}"
        sprint1 = Sprint.objects.create(
            board=board,
            name=sprint1_name,
            start_date=sprint1_start,
            end_date=sprint1_end,
            is_active=False,
        )

        for task_data in sprint_1_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    sprint1,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        # Sprint 2
        sprint2_start = sprint1_end
        sprint2_end = sprint2_start + sprint_duration
        sprint2_name = f"Sprint {sprint2_start.year}.Q{get_quarter(sprint2_start)}.{get_sprint_number_in_quarter(sprint2_start)}"
        sprint2 = Sprint.objects.create(
            board=board,
            name=sprint2_name,
            start_date=sprint2_start,
            end_date=sprint2_end,
            is_active=False,
        )
        for task_data in sprint_2_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    sprint2,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        # Sprint 3
        sprint3_start = sprint2_end
        sprint3_end = sprint3_start + sprint_duration
        sprint3_name = f"Sprint {sprint3_start.year}.Q{get_quarter(sprint3_start)}.{get_sprint_number_in_quarter(sprint3_start)}"
        sprint3 = Sprint.objects.create(
            board=board,
            name=sprint3_name,
            start_date=sprint3_start,
            end_date=sprint3_end,
            is_active=False,
        )
        for task_data in sprint_3_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    sprint3,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        # Sprint 4
        sprint4_start = sprint3_end
        sprint4_end = sprint4_start + sprint_duration
        sprint4_name = f"Sprint {sprint4_start.year}.Q{get_quarter(sprint4_start)}.{get_sprint_number_in_quarter(sprint4_start)}"
        sprint4 = Sprint.objects.create(
            board=board,
            name=sprint4_name,
            start_date=sprint4_start,
            end_date=sprint4_end,
            is_active=False,
        )
        for task_data in sprint_4_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    sprint4,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        # Sprint 5 (Newest - Active)
        sprint5_start = sprint4_end
        sprint5_end = sprint5_start + sprint_duration
        sprint5_name = f"Sprint {sprint5_start.year}.Q{get_quarter(sprint5_start)}.{get_sprint_number_in_quarter(sprint5_start)}"
        sprint5 = Sprint.objects.create(
            board=board,
            name=sprint5_name,
            start_date=sprint5_start,
            end_date=sprint5_end,
            is_active=True,
        )
        for task_data in sprint_5_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    sprint5,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))

        # Non sprint tasks
        for task_data in sample_tasks:
            try:
                self.create_tasks(
                    board,
                    priorities,
                    labels,
                    states,
                    members,
                    estimates,
                    task_data,
                    None,
                    None,
                )

            except Board.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Board with slug "{board_slug}" does not exist')
                )
            except KeyError as e:
                self.stdout.write(
                    self.style.ERROR(f"Missing key in JSON data: {str(e)}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
