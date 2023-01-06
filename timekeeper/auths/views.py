import os

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.models import User

from datetime import datetime


def login_user(req):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if req.user.is_authenticated:
        return redirect(f"/history{current_week}")

    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect(f"/history{current_week}")
        else:
            messages.success(req, ("There was an error loggin in, try again"))
            return redirect("/auths")

    else:
        return render(req, "authenticate/login.html", {})



def logout_user(req):
    if req.user.is_authenticated:
        logout(req)
        messages.success(req, ("Logout successful"))
    return redirect("/auths")


def register_user(req):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"

    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect(f"/history{current_week}")

    if req.method == "POST":
        if req.POST.get("role"):
            is_user_staff = True
        else:
            is_user_staff = False

        password = User.objects.make_random_password()

        registered_user = User.objects.create_user(
            username=req.POST.get("username"),
            first_name=req.POST.get("firstName"),
            last_name=req.POST.get("lastName"),
            email=req.POST.get("email"),
            password=password,
            is_staff=is_user_staff,
        )

        send_register_email(registered_user, password)
        return redirect("/users")
    else:
        return render(req, "authenticate/register.html")


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
