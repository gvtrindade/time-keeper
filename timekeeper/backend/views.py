from django.shortcuts import render, redirect
from .models import Record, User
from datetime import datetime
from django.contrib import messages

# Create your views here.


def index(req):
    return redirect("/auths")


def history(req):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if req.method == "POST":
        record = Record()
        record.user = req.user
        record.status = "Approved"
        record.action = req.POST.get('action')
        record.save()
        return redirect("/history")
    else:
        records = Record.objects.filter(user=req.user).order_by('date__day')
        context = {"records": records, "workedHours": 10}
        return render(req, "backend/history.html", context)


def include(req):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if req.method == "POST":
        record = Record()
        record.user = req.user
        record.date = getDate(req)
        record.action = req.POST.get('action')
        record.save()
        return redirect("/history")
    else:
        return render(req, "backend/include.html")


def getDate(req):
    datetime_str = f'{req.POST.get("date")} {req.POST.get("time")}'
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def userList(req):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect("/history")

    users = User.objects.all
    context = {"users": users}
    return render(req, "backend/userList.html", context)


def user(req, user_id):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect("/history")

    listed_user = User.objects.get(id=user_id)
    if req.method == "POST":
        if req.POST.get("username"):
            listed_user.username = req.POST.get("username")
            listed_user.email = req.POST.get("email")
            if req.POST.get("role"):
                listed_user.is_staff = True
            else:
                listed_user.is_staff = False
            listed_user.save()
        else:
            record = Record.objects.get(id=req.POST.get("id"))
            record.action = req.POST.get("action")
            record.status = req.POST.get("status")
            record.save()

    records = Record.objects.filter(user=listed_user)
    context = {"listed_user": listed_user, "records": records, "workedHours": 10}
    return render(req, "backend/user.html", context)


def register(req):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect("/history")

    return render(req, "backend/register.html")