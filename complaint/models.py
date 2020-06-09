from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Complaint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderid = models.CharField(max_length=100, default='')
    complaint = models.TextField()
    reply = models.TextField(blank=True, null=True)
    replied = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='notreplied')
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.datetime)
