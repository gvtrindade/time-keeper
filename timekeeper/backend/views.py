from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect

from .models import Record
from auths.models import CustomUser
from datetime import datetime

CURRENT_WEEK = f"month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"


def index(request):
    return redirect("/auths")


def history(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if request.method == "POST":
        user = request.user
        action = request.POST.get("action")
        break_duration = request.POST.get("breakDuration")

        record = Record()
        record.create_record(user, "Approved", action, break_duration=break_duration)


        return redirect(f"/history?{CURRENT_WEEK}")
    else:
        user = request.user
        year = int(request.GET.get('year'))
        number = int(request.GET.get('number'))
        is_month = request.GET.get('month') == 'true'

        try:
            record = Record()
            records = record.get_records(user, year, number, is_month)
            earliest_record = (
                Record.objects.filter(user=request.user).earliest(
                    "date__year").date.year
            )
            context = {
                "records": records,
                "workedHours": record.calculate_worked_hours(records),
                "years": range(earliest_record, datetime.now().year + 1),
            }
        except:
            context = {
                "records": [],
                "years": range(datetime.now().year, datetime.now().year + 1),
            }

        context = {
            **context,
            "isHistory": True,
            "year": year,
            "month": request.GET.get("month"),
            "number": number,
            "range": range(1, 13) if is_month else range(1, 53),
        }
        return render(request, "backend/history.html", context)


def include(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if request.method == "POST":
        user = request.user
        date = request.POST.get("date")
        clockin_time = request.POST.get("clockInTime")
        clockout_time = request.POST.get("clockOutTime")
        break_duration = request.POST.get("breakDuration") or 0
        remarks = request.POST.get("remarks")

        record = Record()

        if (clockin_time):
            record.create_record(
                user, "Wating Approval", 'Clock-in', date, clockin_time, break_duration, remarks)

        if (clockout_time):
            record.create_record(
                user, "Wating Approval", 'Clock-out', date, clockout_time, break_duration, remarks)
        return redirect(f"/history?{CURRENT_WEEK}")
    else:
        return render(request, "backend/include.html")


def user_list(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history?{CURRENT_WEEK}")

    users = CustomUser.objects.all
    context = {"users": users}
    return render(request, "backend/userList.html", context)


def user(request, user_id):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history?{CURRENT_WEEK}")

    listed_user = CustomUser.objects.get(id=user_id)
    record = Record()

    if request.method == "POST":
        if request.POST.get("username"):
            listed_user.username = request.POST.get("username")
            listed_user.first_name = request.POST.get("firstName")
            listed_user.last_name = request.POST.get("lastName")
            listed_user.email = request.POST.get("email")
            if request.POST.get("role"):
                listed_user.is_staff = True
            else:
                listed_user.is_staff = False
            listed_user.save()
        else:
            edited_record = Record.objects.get(id=request.POST.get("id"))
            date = request.POST.get("date")
            time = request.POST.get("time")
            time_period = request.POST.get("timePeriod")
            edited_record.date = record.get_date(date, time)
            edited_record.action = request.POST.get("action")
            edited_record.status = request.POST.get("status")
            edited_record.save()

    try:
        year = int(request.GET.get('year'))
        number = int(request.GET.get('number'))
        is_month = request.GET.get('month') == 'true'
        records = record.get_records(listed_user, year, number, is_month)
        earliest_record = (
            Record.objects.filter(user=listed_user).earliest(
                "date__year").date.year
        )

        context = {
            "listed_user": listed_user,
            "records": records,
            "workedHours": record.calculate_worked_hours(records),
            "years": range(earliest_record, datetime.now().year + 1),
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
        "year": request.GET.get("year"),
        "month": request.GET.get("month"),
        "number": request.GET.get("number"),
        "range": range(1, 13) if request.GET.get("month") == "true" else range(1, 53),
    }

    return render(request, "backend/user.html", context)


def delete_record(request, record_id):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    if request.method == "DELETE":
        print("Record: ", record_id)
        record = Record.objects.get(pk=record_id)
        record.delete()
        return HttpResponseRedirect("/history")


def handler404(request, exception):
    context = {"error_code": 404}
    return render(request, "backend/error.html", context)


def handler403(request, exception):
    context = {"error_code": 403}
    return render(request, "backend/error.html", context)


def handler500(request, exception=''):
    context = {"error_code": 500}
    return render(request, "backend/error.html", context)
