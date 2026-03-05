# models.py
from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    time_spent = models.CharField(max_length=50)
    late_entries = models.IntegerField()
    early_exits = models.IntegerField()
    attendance_status = models.CharField(max_length=50)
    threshold_alert = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return self.name
