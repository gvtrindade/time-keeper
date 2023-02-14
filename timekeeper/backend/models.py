from django.db import models
from django.utils.timezone import now

from auths.models import CustomUser


class Record(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)
    action = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=20, default='Wating Approval')
    break_duration = models.IntegerField(default=0)
    remarks = models.CharField(max_length=255, default='')