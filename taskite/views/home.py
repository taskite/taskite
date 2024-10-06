from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from django.views import View
from django.core.files.storage import default_storage
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_verified:
            # Redirect them to email verification page
            return redirect("accounts-verify")

        if request.user.current_workspace:
            return redirect(
                "workspaces-dashboard",
                workspace_slug=request.user.current_workspace.slug,
            )
        
        workspace = request.user.workspaces.first()
        if not workspace:
            return redirect("home-create")

        return redirect("workspaces-dashboard", workspace_slug=workspace.slug)


class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/create.html")


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, *args, **kwargs):
        file = request.data["file"]
        # Save the file using default storage
        default_storage.save(kwargs.get("file_key"), file)
        # ...
        return Response(status=204)
