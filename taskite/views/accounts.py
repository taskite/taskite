from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import serializers

from taskite.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "username"]


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
        return render(request, "accounts/register.html")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("accounts-login")


class VerifyView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/verify.html")


class VerifyConfirmView(View):
    def get(self, request, verification_id):
        user = User.objects.filter(verification_id=verification_id).first()
        if not user:
            raise Http404
        
        user.verify_confirm()
        login(request, user)
        return redirect("home-index")