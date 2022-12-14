from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Record(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  date = models.DateTimeField()
  status = models.CharField(max_length=20, default='Wating Approval')