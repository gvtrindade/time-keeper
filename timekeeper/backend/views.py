from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Record
from datetime import datetime, timedelta


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
        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")

    else:
        try:
            records = getRecords(req)
            earliest_Record = (
                Record.objects.filter(user=req.user).earliest("date__year").date.year
            )
            context = {
                "records": records,
                "workedHours": calculateWorkedHours(records),
                "years": range(earliest_Record, datetime.now().year + 1),
            }
        except:
            context = {
                "records": [],
                "years": range(datetime.now().year, datetime.now().year + 1),
            }

        context = { 
            **context,
            "isHistory": True,
            "year": req.GET.get("year"),
            "month": req.GET.get("month"),
            "number": req.GET.get("number"),
            "range": range(1, 13) if req.GET.get("month") == "true" else range(1, 53),
        }
        context.update()
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
        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")

    else:
        return render(req, "backend/include.html")


def getDate(req):
    datetime_str = f'{req.POST.get("date")} {req.POST.get("time")}'
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def userList(req):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect(f"/history{current_week}")

    users = User.objects.all
    context = {"users": users}
    return render(req, "backend/userList.html", context)


def user(req, user_id):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if not req.user.is_authenticated:
        messages.success(req, ("You must login to access this page"))
        return redirect("/auths")

    if not req.user.is_staff:
        messages.success(req, ("You can't access this page"))
        return redirect(f"/history{current_week}")

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
            record.status = req.POST.get("status")
            record.save()

    try:
        records = getRecords(req)
        earliest_Record = (
            Record.objects.filter(user=listed_user).earliest("date__year").date.year
        )

        context = {
            "listed_user": listed_user,
            "records": records,
            "workedHours": calculateWorkedHours(records),
            "years": range(earliest_Record, datetime.now().year + 1),
        }
    except:
        context = {
            "records": [],
            "years": range(datetime.now().year, datetime.now().year + 1),
        }

    context = {
        **context,
        "listed_user": listed_user,
        "isHistory": False,
        "year": req.GET.get("year"),
        "month": req.GET.get("month"),
        "number": req.GET.get("number"),
        "range": range(1, 13) if req.GET.get("month") == "true" else range(1, 53),
    }

    return render(req, "backend/user.html", context)


def getRecords(req):
    year = req.GET.get("year") if req.GET.get("year") else datetime.now().year
    number = (
        req.GET.get("number")
        if req.GET.get("number")
        else datetime.now().strftime("%V")
    )
    query = Q(user=req.user, date__year=int(year))

    if req.GET.get("month") == "true":
        query.add(Q(date__month=int(number)), "AND")
    else:
        query.add(Q(date__week=int(number)), "AND")

    return Record.objects.filter(query).order_by("date__day", "date__hour")


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
        if record_index + 1 < len(records) and (
            records[record_index].date.day == records[record_index + 1].date.day
            and records[record_index + 1].action == "Clock-out"
            and records[record_index + 1].status == "Approved"
        ):
            worked_hours += records[record_index + 1].date - records[record_index].date

    worked_seconds = worked_hours.seconds
    return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)


def delete_record(req, record_id):
    if req.method == "DELETE":
        print("Record: ", record_id)
        record = Record.objects.get(pk=record_id)
        record.delete()
        return HttpResponseRedirect("/history")


def delete_user(req, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return HttpResponseRedirect("/users")
