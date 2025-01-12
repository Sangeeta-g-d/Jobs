from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from . models import *
# Create your views here.

def v3_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None and user.is_superuser == True:
            login(request,user)
            return redirect('/admin_db')
        else:
            error_message = "Invalid username or password"
            return render(request,'v3_login.html',{'error_message':error_message})
    return render(request,'v3_login.html')

def admin_db(request):
    return render(request,'admin_db.html')

def job_details(request):
    data= Jobs.objects.all()
    context = {
        'data':data
    }
    return render(request,'job_details.html',context)


def admin_logout(request):
    logout(request)
    return redirect('/admin_login')

def register(request):
    return render(request,'register.html')

def add_job(request):
    if request.method == 'POST':
        added_by = request.user  # Get the NewUser instance directly
        job_title = request.POST.get('job_title')
        experience = request.POST.get('experience')
        salary = request.POST.get('package')  # Ensure 'package' is correctly mapped
        education = request.POST.get('education')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        .
        work_mode = request.POST.get('work_mode')
        r_and_r = request.POST.get('r_and_r')
        jon_link = request.POST.get('job_link')
        company_name = request.POST.get('company_name')
        required_skills = request.POST.get('skills')  # Ensure 'skills' is correctly mapped

        # Create the job entry
        job = Jobs.objects.create(
            job_title=job_title,
            salary=salary,
            experience=experience,
            education=education,
            location=location,
            job_type=job_type,
            work_mode=work_mode,
            required_skills=required_skills,
            roles_and_responsibilities=r_and_r,
            jon_link=jon_link,
            company_name=company_name,
            added_by=added_by,  # Use the instance
        )
        return redirect('/add_job')

    return render(request, 'add_job.html')