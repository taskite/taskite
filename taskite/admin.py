from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from taskite.models import (
    User,
    Board,
    BoardMembership,
    State,
    Task,
    TaskAssignee,
    Priority,
    Workspace,
    WorkspaceMembership,
    Team,
    TeamMembership,
    WorkspaceInvite,
    Upload,
    PurgedAsset,
    UnusedAsset,
)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            "email",
            "username",
        ]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "username", "is_admin"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["email", "username", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            "Personal info",
            {"fields": ["username", "first_name", "last_name", "avatar"]},
        ),
        ("Permissions", {"fields": ["is_admin", "verified_at", "verification_id"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "username",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


class WorkspaceMembershipAdmin(admin.StackedInline):
    model = WorkspaceMembership
    extra = 0


class WorkspaceInviteInlineAdmin(admin.StackedInline):
    model = WorkspaceInvite
    extra = 0


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]
    raw_id_fields = ["created_by"]
    inlines = [WorkspaceMembershipAdmin, WorkspaceInviteInlineAdmin]


class BoardMembershipAdmin(admin.StackedInline):
    model = BoardMembership
    extra = 1


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ["name", "created_by"]
    raw_id_fields = ["created_by"]
    inlines = [BoardMembershipAdmin]


class TeamMembershipInline(admin.StackedInline):
    model = TeamMembership
    extra = 1


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "created_at"]
    inlines = [TeamMembershipInline]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at"]


class TaskAssigneeInlineAdmin(admin.StackedInline):
    model = TaskAssignee
    extra = 1


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "summary", "created_at"]
    inlines = [TaskAssigneeInlineAdmin]


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ["id", "key", "filename", "confirmed_at", "deleted_at", "created_at"]


@admin.register(UnusedAsset)
class UnunsedAssetAdmin(admin.ModelAdmin):
    list_display = ["key", "bucket", "created_at"]


@admin.register(PurgedAsset)
class PurgeAssetAdmin(admin.ModelAdmin):
    list_display = ["key", "bucket", "purged_at"]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
