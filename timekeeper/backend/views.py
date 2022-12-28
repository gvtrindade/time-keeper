from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from datetime import datetime, timedelta
from .models import Record

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
        record.action = req.POST.get("action")
        record.save()
        return redirect("/history")
    else:
        records = Record.objects.filter(user=req.user).order_by("date__day")
        context = {"records": records, "workedHours": calculateWorkedHours(records)}
        return render(req, "backend/history.html", context)


def include(req):
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if req.method == "POST":
        record = Record()
        record.user = req.user
        record.date = getDate(req)
        record.action = req.POST.get("action")
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

    records = Record.objects.filter(user=listed_user).order_by("date__day")
    context = {
        "listed_user": listed_user,
        "records": records,
        "workedHours": calculateWorkedHours(records),
    }
    return render(req, "backend/user.html", context)


def calculateWorkedHours(records):
    worked_hours = timedelta(0)
    check_in_records = list(
        filter(
            lambda record: record.action == "Clock-in" and record.status == "Approved",
            records,
        )
    )

    for record in check_in_records:
        record_index = next(i for i, x in enumerate(list(records)) if x.id == record.id)
        if record_index + 1 < len(records):
            if (
                records[record_index].date.day == records[record_index + 1].date.day
                and records[record_index + 1].action == "Clock-out"
                and records[record_index + 1].status == "Approved"
            ):
                worked_hours += (
                    records[record_index + 1].date - records[record_index].date
                )

    worked_seconds = worked_hours.seconds
    return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)

