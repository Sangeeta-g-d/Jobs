from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class NewUser(AbstractUser):
    user_type = models.CharField(max_length=100, default='user')
    fullname= models.CharField(max_length=250, blank=True)
    phone_no = models.CharField(max_length=100, blank=True)


class Jobs(models.Model):
    added_by = models.ForeignKey(NewUser, on_delete=models.CASCADE, default='')
    job_title = models.CharField(max_length=200)
    salary = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=300, blank=True)
    education = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)
    job_type = models.CharField(max_length=500, blank=True)
    work_mode = models.CharField(max_length=500, blank=True)
    required_skills = models.CharField(max_length=900)
    roles_and_responsibilities = models.CharField(max_length=1500, blank=True)
    job_link = models.CharField(max_length=400, default='nolink')
    company_name = models.CharField(max_length=300, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)  # New field

    def __str__(self):
        return self.job_title
