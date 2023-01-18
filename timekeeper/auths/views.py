import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from datetime import datetime

from .forms import PasswordChangingForm
from .models import CustomUser


def login_user(request):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if request.user.is_authenticated:
        return redirect(f"/history{current_week}")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            userData = CustomUser.objects.get(id=request.user.id)
            if not userData.is_resetpwd:
                return redirect("/auths/password")
            return redirect(f"/history{current_week}")
        else:
            messages.success(
                request, ("There was an error loggin in, try again"))
            return redirect("/auths")

    else:
        return render(request, "auths/login.html", {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, ("Logout successful"))
    return redirect("/auths")


def register_user(request):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"

    if not request.user.is_authenticated:
        messages.success(request, ("You must login to access this page"))
        return redirect("/auths")

    if not request.user.is_staff:
        messages.success(request, ("You can't access this page"))
        return redirect(f"/history{current_week}")

    if request.method == "POST":
        if request.POST.get("role"):
            is_user_staff = True
        else:
            is_user_staff = False

        password = CustomUser.objects.make_random_password()

        registered_user = CustomUser.objects.create_user(
            username=request.POST.get("username"),
            first_name=request.POST.get("firstName"),
            last_name=request.POST.get("lastName"),
            email=request.POST.get("email"),
            password=password,
            is_staff=is_user_staff,
        )

        send_register_email(registered_user, password)
        return redirect("/users")
    else:
        return render(request, "auths/register.html")


def send_register_email(user, password):
    send_mail(
        "Welcome to The Pleasaunce team!",
        f"We are very happy to have out volunteer with us, {user.first_name} {user.last_name}! \n"
        + f"\n"
        + f"Here are your credentials: \n"
        + f"Username: {user.username}\n"
        + f"Password: {password}\n"
        + f"\n"
        + f"You will have to create a new password upon your first login!",
        str(os.getenv("EMAIL_HOST_USER")),
        recipient_list=[user.email],
        fail_silently=False,
    )


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    success_url = f"/history{current_week}"

    def form_valid(self, form):
        form.user.is_resetpwd = True
        return super().form_valid(form)
