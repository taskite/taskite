from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_verified:
            # Redirect them to email verification page
            return redirect("accounts-verify")
        workspace = request.user.workspaces.first()
        if not workspace:
            return redirect("home-create")

        return redirect("workspaces-dashboard", workspace_slug=workspace.slug)


class CreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "home/create.html")
