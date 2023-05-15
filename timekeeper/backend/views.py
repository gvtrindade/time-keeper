from datetime import datetime

from auths.models import CustomUser
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .models import Record

CURRENT_WEEK = f"year={datetime.now().year}&month={datetime.now().month}&week={datetime.now().strftime('%V')}"

MONTHS = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December',
}

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
        save_record(request)
        return redirect(f"/history?{CURRENT_WEEK}")
    else:
        context = query_records(request)

        context = {
            **context,
            "isHistory": True,
        }
        return render(request, "backend/history.html", context)


def query_records(request):
    user = request.user
    year = int(request.GET.get('year'))
    week = int(request.GET.get('week'))
    month = int(request.GET.get('month'))

    try:
        record = Record()
        passed_month = month if week == -1 else None
        records = record.get_records(user, year, week, passed_month)
        earliest_record = (
            Record.objects.filter(user=request.user).earliest(
                "date__year").date.year
        )
        options = record.get_filter_options(year, month)

        context = {
            "records": records,
            "workedHours": record.calculate_worked_hours(records),
            "years": range(earliest_record, datetime.now().year + 1),
            "selectedYear": year,
            "months": MONTHS,
            "selectedMonth": month,
            "selectedWeek": week,
            "options": options
        }
    except:
        context = {
            "records": [],
            "years": range(datetime.now().year, datetime.now().year + 1),
            "selectedYear": year,
            "months": MONTHS,
            "selectedMonth": month,
            "selectedWeek": week,
            "options": {}
        }

    return context


def save_record(request):
    user = request.user
    action = request.POST.get("action")
    break_duration = request.POST.get("breakDuration")

    record = Record()
    record.create_record(user, "Approved", action,
                         break_duration=break_duration)


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

        if clockin_time:
            record.create_record(
                user, "Wating Approval", 'Clock-in', date, clockin_time, break_duration, remarks)

        if clockout_time:
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
            edited_record.date = record.get_date(date, time)
            edited_record.action = request.POST.get("action")
            edited_record.status = request.POST.get("status")
            edited_record.save()

    try:
        year = int(request.GET.get('year'))
        week = int(request.GET.get('week'))
        month = int(request.GET.get('month'))
        passed_month = month if week == -1 else None
        records = record.get_records('', year, week, passed_month)
        earliest_record = (
            Record.objects.filter(user=listed_user).earliest(
                "date__year").date.year
        )
        options = record.get_filter_options(year, month)

        context = {
            "listed_user": listed_user,
            "records": records,
            "workedHours": record.calculate_worked_hours(records),
            "years": range(earliest_record, datetime.now().year + 1),
            "selectedYear": year,
            "months": MONTHS,
            "selectedMonth": month,
            "selectedWeek": week,
            "options": options
        }
    except:
        context = {
            "records": [],
            "years": range(datetime.now().year, datetime.now().year + 1),
            "selectedYear": year,
            "months": MONTHS,
            "selectedMonth": month,
            "selectedWeek": week,
            "options": {}
        }

    context = {
        **context,
        "listed_user": listed_user,
        "isHistory": False,
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
