from django.db import models
from django.utils import timezone


class Record(models.Model):
    em_id = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    clocked_time = models.DateTimeField(default=timezone.now)
    clocking_type = models.BooleanField(default=False)
    remark = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return (f"{self.em_id}")


class Employee(models.Model):
    em_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.em_id}")


class EmployeeRecord(models.Model):
    em_id = models.CharField(max_length=20)
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return (f"{self.em_id}")


class FileUpload(models.Model):
    file = models.FileField(upload_to='load_to_db')
