from django.db import models
from django.utils import timezone

class Log(models.Model):
    LogId = models.AutoField(primary_key=True)
    Message = models.CharField(max_length=200, null=True, default='')
    LogLevel = models.CharField(max_length=50)
    Category = models.CharField(max_length=50)
    Timestamp = models.DateTimeField(auto_now=True)
    Operation = models.CharField(max_length=50, null=True, default=None)
    Success = models.IntegerField(max_length=1, null=True, default=None)
    UserId = models.CharField(max_length=100, null=True)
    SessionId = models.CharField(max_length=50, null=True)