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

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.SIXTY_SECONDS = 60
        self.ZERO_HOUR = 0
        self.TWELVE_HOURS = 12
        self.TWENTY_FOUR_HOURS = 24

    def get_records(self, user, year=datetime.now().year, number=datetime.now().strftime("%V"), is_month=False):
        query = Q(user=user, date__year=year)

        if is_month:
            query.add(Q(date__month=number), "AND")
        else:
            query.add(Q(date__week=number), "AND")

        return Record.objects.filter(query).order_by("date__day", "date__hour")

    def create_record(self, user, status, action, date=None, time=None, time_period=None, break_duration=0, remarks=None):
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
            (break_duration_sum * self.SIXTY_SECONDS)

        return "{:02}h{:02}".format(worked_seconds // 3600, worked_seconds % 3600 // 60)
