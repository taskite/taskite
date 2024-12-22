from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import serializers

from calyvim.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "display_name", "username"]


class LoginView(View):
    def get(self, request):
        next = request.GET.get("next", "/")
        context = {
            "props": {
                "next": next,
            }
        }
        return render(request, "accounts/login.html", context)


class RegisterView(View):
    def get(self, request):
        context = {"props": {"invitation_id": request.GET.get("invitation_id", None)}}
        return render(request, "accounts/register.html", context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts-login")
    

class GoogleOAuthView(View):
    def get(self, request):
        pass


class VerifyView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_verified:
            return redirect("accounts-login")
        
        context = {
            "props": {
                "current_user": UserSerializer(request.user).data,
            }
        }

        return render(request, "accounts/verify.html", context)


class VerifyConfirmView(View):
    def get(self, request, verification_id):
        user = User.objects.filter(verification_id=verification_id).first()
        if not user:
            raise Http404

        user.verify_confirm()
        login(request, user)
        return redirect("workspace-index")


class ResetView(View):
    def get(self, request):
        return render(request, "accounts/reset.html")


class ResetConfirmView(View):
    def get(self, request, password_reset_id):
        user = User.objects.filter(password_reset_id=password_reset_id).first()
        if not user:
            raise Http404()

        context = {"props": {"password_reset_id": password_reset_id}}
        return render(request, "accounts/reset_confirm.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html")


class SecurityView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/security.html")
    