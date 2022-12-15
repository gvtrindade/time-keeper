from django.shortcuts import render, redirect
from .models import Record, User
from datetime import datetime

# Create your views here.


def index(req):
    return redirect("/auths")


def history(req):
    if req.method == "POST":
        record = Record()
        record.user = req.user
        record.status = "Approved"
        record.save()
        return redirect("/history")
    else:
        records = Record.objects.filter(user=req.user)
        context = {"records": records, "workedHours": 10}
        return render(req, "backend/history.html", context)


def include(req):
    if req.method == "POST":
        record = Record()
        record.user = req.user
        record.date = getDate(req)
        record.save()
        return redirect("/history")
    else:
        return render(req, "backend/include.html")


def getDate(req):
    datetime_str = f'{req.POST.get("date")} {req.POST.get("time")}'
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def userList(req):
    users = User.objects.all
    context = {"users": users}
    return render(req, "backend/userList.html", context)


def user(req, user_id):
    user = User.objects.get(id=user_id)
    records = Record.objects.filter(user=user)
    context = {"user": user, "records": records, "workedHours": 10}
    return render(req, "backend/user.html", context)


def register(req):
    # if not req.user.is_authenticated:
    #     return render(req, "backend/error.html")

    return render(req, "backend/register.html")
