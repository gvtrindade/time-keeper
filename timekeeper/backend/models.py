import calendar
from datetime import datetime, timedelta
from django.db import models
from django.db.models import Q
from django.utils.timezone import now


from auths.models import CustomUser


class Record(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    action = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=20, default='Wating Approval')
    break_duration = models.IntegerField(default=0)
    remarks = models.CharField(max_length=255, default='')
    off_day = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.sixty_seconds = 60
        self.zero_hour = 0
        self.twelve_hours = 12
        self.twenty_four_hours = 24

    def get_records(self, user, year=datetime.now().year, week=int(datetime.now().strftime("%V")), month=None):
        query = Q(user=user, date__year=year)

        if month:
            query.add(Q(date__month=month), "AND")
        else:
            query.add(Q(date__week=week), "AND")

        return Record.objects.filter(query).order_by("date__day", "date__hour")

    def create_record(self, user, status, action, date=None, time=None, break_duration=0, remarks=None):
        record = Record()
        record.user = user
        record.status = status
        record.action = action
        if action == "Clock-out":
            record.break_duration = break_duration

        if date:
            record.date = self.get_date(date, time)

        if remarks:
            record.remarks = remarks

        record.save()

    def create_off_day(self, username, date):
        user = CustomUser.objects.filter(username=username)[0]
        
        off_day = Record()
        off_day.user = user
        off_day.date = self.get_date(date, "00:00")
        off_day.off_day = True
        off_day.status = 'Approved'
        off_day.save()

    def get_date(self, date, time):
        datetime_str = f'{date} {time}'
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

    def calculate_worked_hours(self, records):
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
            (break_duration_sum * self.sixty_seconds)

        return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)

    def get_weeks_in_month(self, year, month):
        first_week = int(datetime(year, month, 1).strftime('%V'))
        last_day_of_month = calendar.monthrange(year, month)[1]
        last_week = int(datetime(year, month, last_day_of_month).strftime('%V')) + 1

        return [*range(first_week, last_week)]

    def get_week_days(self, year, week_number):
        date = f'{year}-W{week_number}'
        reference_day = datetime.strptime(date + '-1', "%Y-W%W-%w")
        fist_day = self.ordinal_number(reference_day.day)

        reference_day = reference_day + timedelta(days=6)
        last_day = self.ordinal_number(reference_day.day)

        return f'{fist_day} - {last_day}'

    def ordinal_number(self, number):
        suffix = None
        match number:
            case 1 | 21 | 31:
                suffix = 'st'
            case 2 | 22:
                suffix = 'nd'
            case 3 | 23:
                suffix = 'rd'
            case _:
                suffix = 'th'
        return f'{number}{suffix}'

    def get_filter_options(self, year, month):
        options = {}
        weeks = self.get_weeks_in_month(year, month)
        for week in weeks:
            week_days = self.get_week_days(year, week)
            options[week] = week_days
        return options
    