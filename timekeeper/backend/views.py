from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect

from .models import Record
from auths.models import CustomUser
from datetime import datetime, timedelta


def index(request):
    return redirect("/auths")


def history(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(request, "You must reset your password before accessing the application")
        return redirect("/auths/password")

    if request.method == "POST":
        record = Record()
        record.user = request.user
        record.status = "Approved"
        record.action = request.POST.get("action")
        record.save()
        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")

    else:
        try:
            records = get_records(request)
            earliest_record = (
                Record.objects.filter(user=request.user).earliest(
                    "date__year").date.year
            )
            context = {
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
            "isHistory": True,
            "year": request.GET.get("year"),
            "month": request.GET.get("month"),
            "number": request.GET.get("number"),
            "range": range(1, 13) if request.GET.get("month") == "true" else range(1, 53),
        }
        return render(request, "backend/history.html", context)


def include(request):
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(request, "You must reset your password before accessing the application")
        return redirect("/auths/password")

    if request.method == "POST":
        record = Record()
        record.user = request.user
        record.date = get_date(request)
        record.action = request.POST.get("action")
        record.save()
        current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
        return redirect(f"/history{current_week}")

    else:
        return render(request, "backend/include.html")


def get_date(request):
    datetime_str = f'{request.POST.get("date")} {request.POST.get("time")}'
    return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")


def user_list(request):
    current_week = f"?month=false&year={datetime.now().year}&number={datetime.now().strftime('%V')}"
    if not request.user.is_authenticated:
        messages.success(request, "You must login to access this page")
        return redirect("/auths")
    elif not request.user.is_password_reset:
        messages.success(request, "You must reset your password before accessing the application")
        return redirect("/auths/password")

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
        messages.success(request, "You must reset your password before accessing the application")
        return redirect("/auths/password")

    if not request.user.is_staff:
        messages.success(request, "You can't access this page")
        return redirect(f"/history{current_week}")

    listed_user = CustomUser.objects.get(id=user_id)
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
            record = Record.objects.get(id=request.POST.get("id"))
            record.status = request.POST.get("status")
            record.save()

    try:
        records = get_records(request)
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


def calculate_worked_hours(records):
    worked_hours = timedelta(0)
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

    worked_seconds = worked_hours.seconds
    return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)


def delete_record(request, record_id):
    if request.method == "DELETE":
        print("Record: ", record_id)
        record = Record.objects.get(pk=record_id)
        record.delete()
        return HttpResponseRedirect("/history")


def delete_user(user_id):
    deleted_user = CustomUser.objects.get(pk=user_id)
    deleted_user.delete()
    return HttpResponseRedirect("/users")


def handler404(request, exception):
    context = {"error_code": 404}
    return render(request, "backend/error.html", context)


def handler403(request, exception):
    context = {"error_code": 403}
    return render(request, "backend/error.html", context)


def handler500(request, exception=''):
    context = {"error_code": 500}
    return render(request, "backend/error.html", context)
