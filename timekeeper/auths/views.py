import os
from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from .forms import PasswordChangingForm, PasswordResettingForm, PasswordResettingConfirmForm
from .models import CustomUser

CURRENT_WEEK = f"?year={datetime.now().year}&month={datetime.now().month}&week={datetime.now().strftime('%V')}"

def login_user(request):
    if request.user.is_authenticated:
        return redirect(f"/history{CURRENT_WEEK}")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if not user.is_password_reset:
                messages.success(
                    request, "You must reset your password before accessing the application")
                return redirect("/auths/change-password")
            return redirect(f"/history{CURRENT_WEEK}")
        else:
            messages.success(
                request, "There was an error logging in, try again")
            return redirect("/auths")

    else:
        return render(request, "auths/login.html", {})


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout successful")
    return redirect("/auths")


def register_user(request):

    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history{CURRENT_WEEK}")

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


def delete_user(request, user_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    if request.method == "DELETE":
        deleted_user = CustomUser.objects.get(pk=user_id)
        deleted_user.delete()
        return HttpResponseRedirect("/users")


def send_register_email(user, password):
    send_mail(
        "Welcome to The Pleasaunce team!",
        f"Welcome to The Pleasaunce team! \n"
        + f"\n"
        + f"We are very happy to have out volunteer with us, {user.first_name} {user.last_name}! \n"
        + f"\n"
        + f"Here are your credentials: \n"
        + f"Username: {user.username}\n"
        + f"Password: {password}\n"
        + f"\n"
        + f"You will have to register a new password upon your first login!\n"
        + f"\n"
        + f"You can start registering your activities at: \n"
        + f"https://timekeeper.pythonanywhere.com/",
        str(os.getenv("EMAIL_HOST_USER")),
        recipient_list=[user.email],
        fail_silently=False,
    )


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = f"/history{CURRENT_WEEK}"

    def form_valid(self, form):
        form.user.is_password_reset = True
        return super().form_valid(form)


class PasswordsResetView(PasswordResetView):
    form_class = PasswordResettingForm
    success_url = "/auths/reset-password-success"


def reset_password_success(request):
    return render(request, "auths/reset-password-success.html")


def reset_password_complete(request):
    return render(request, "auths/reset-password-complete.html")
