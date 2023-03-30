from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Record
from auths.models import CustomUser
from datetime import datetime, timedelta

SIXTY_SECONDS = 60
ZERO_HOUR = 0
TWELVE_HOURS = 12
TWENTY_FOUR_HOURS = 24


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
        status = "Wating Approval" if request.POST.get("date") else "Approved"
        action = request.POST.get("action")
        break_duration = request.POST.get("breakDuration")

        record = Record()
        record.create_record(user, status, action,
                             break_duration=break_duration)

        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")
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
        status = "Wating Approval" if request.POST.get("date") else "Approved"
        action = request.POST.get("action")
        break_duration = request.POST.get("breakDuration")
        date = request.POST.get("date")
        time = request.POST.get("time")
        time_period = request.POST.get("timePeriod")
        remarks = request.POST.get("remarks")

        record = Record()
        record.create_record(user, status, action, date,
                             time, time_period, break_duration, remarks)

        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")
    else:
        return render(request, "backend/include.html")


def user_list(request):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history{current_week}")

    users = CustomUser.objects.all
    context = {"users": users}
    return render(request, "backend/userList.html", context)


def user(request, user_id):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(
            request, "You must reset your password before accessing the application")
        return redirect("/auths/change-password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history{current_week}")

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
            edited_record.date = record.get_date(date, time, time_period)
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
            "workedHours": calculate_worked_hours(records),
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


def get_date(request):
    time = request.POST.get("time")
    time_period = request.POST.get("timePeriod")
    if time_period == "PM":
        hours = ZERO_HOUR if int(
            time[:2]) + TWELVE_HOURS == TWENTY_FOUR_HOURS else int(time[:2]) + TWELVE_HOURS
        minutes = time[3:]
        time = f'{hours}:{minutes}'
    datetime_str = f'{request.POST.get("date")} {time}'
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def get_records(request):
    year = request.GET.get("year") if request.GET.get(
        "year") else datetime.now().year
    number = (
        request.GET.get("number")
        if request.GET.get("number")
        else datetime.now().strftime("%V")
    )
    query = Q(user=request.user, date__year=int(year))

    if request.GET.get("month") == "true":
        query.add(Q(date__month=int(number)), "AND")
    else:
        query.add(Q(date__week=int(number)), "AND")

    return Record.objects.filter(query).order_by("date__day", "date__hour")


def create_record(request):
    record = Record()
    record.user = request.user
    record.status = "Wating Approval" if request.POST.get(
        "date") else "Approved"
    record.action = request.POST.get("action")
    if request.POST.get("date"):
        record.date = get_date(request)
    if request.POST.get("remarks"):
        record.remarks = request.POST.get("remarks")
    if record.action == "Clock-out":
        record.break_duration = request.POST.get("breakDuration")
    record.save()


def calculate_worked_hours(records):
    worked_hours = timedelta(0)
    break_duration_sum = 0
    check_in_records = list(
        filter(
            lambda record: record.action == "Clock-in" and record.status == "Approved",
            records,
        )
    )

    for record in check_in_records:
        record_index = next(i for i, x in enumerate(
            list(records)) if x.id == record.id)

        if record_index + 1 < len(records) and (
                records[record_index].date.day == records[record_index + 1].date.day
                and records[record_index + 1].action == "Clock-out"
                and records[record_index + 1].status == "Approved"
        ):
            worked_hours += records[record_index +
                                    1].date - records[record_index].date
            break_duration_sum += records[record_index + 1].break_duration

    worked_seconds = worked_hours.seconds - \
        (break_duration_sum * SIXTY_SECONDS)

    return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)


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
