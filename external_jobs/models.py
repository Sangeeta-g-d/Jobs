from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class NewUser(AbstractUser):
    user_type = models.CharField(max_length=100, default='user')
    fullname= models.CharField(max_length=250, blank=True)
    phone_no = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=500, blank=True)  # New field for address
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # New field for profile image

    def __str__(self):
        return self.username

class UserDetails(models.Model):
    user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100, default='qualification')
    year_of_exp = models.CharField(max_length=250, default='exp')
    area_of_interest = models.CharField(max_length=250, default='interest')
    year_of_passing = models.CharField(max_length=100,default='year')
    user_resume = models.FileField(upload_to='user_resumes/',blank=True, null=True)
    skills = models.CharField(max_length=700,default='skills')


class Jobs(models.Model):
    added_by = models.ForeignKey(NewUser, on_delete=models.CASCADE, default='')
    job_title = models.CharField(max_length=200)
    salary = models.CharField(max_length=200, blank=True)
    experience = models.CharField(max_length=300, blank=True)
    education = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=500, blank=True)
    job_type = models.CharField(max_length=500, blank=True)
    work_mode = models.CharField(max_length=500, blank=True)
    category = models.CharField(max_length=500, blank=True)
    required_skills = models.CharField(max_length=900)
    roles_and_responsibilities = models.CharField(max_length=1500, blank=True)
    job_link = models.CharField(max_length=400, default='nolink')
    company_name = models.CharField(max_length=300, blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    status = models.CharField(max_length=400, default='Active')
    # New field to store the job posting date
    date_posted = models.DateField(auto_now_add=True)  # Stores only date (not time)

    def __str__(self):
        return self.job_title
    
class AppliedJob(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    company = models.IntegerField()  # Store company ID
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE) # Store job ID
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)


class Contact_us(models.Model):
    name = models.CharField(max_length=500, blank=True)
    email= models.CharField(max_length=250, blank=True)
    phone_no = models.CharField(max_length=100, blank=True)
    message = models.CharField(max_length=5000, blank=True)  # New field for address
