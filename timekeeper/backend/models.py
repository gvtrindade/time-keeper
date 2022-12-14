from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Record(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField(default=now)
  status = models.CharField(max_length=20, default='Wating Approval')