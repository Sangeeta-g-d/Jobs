from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from . models import *
from django.contrib import messages
from django.http import JsonResponse
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

def add_job(request):
    return render(request,'add_job.html')

def admin_logout(request):
    logout(request)
    return redirect('/admin_login')

def register(request):
    return render(request,'register.html')

def add_job(request):
    if request.method == 'POST':
        try:
            # Extracting form data
            added_by = request.user
            job_title = request.POST.get('job_title', '').strip()
            experience = request.POST.get('experience', '').strip()
            salary = request.POST.get('package', '').strip()
            education = request.POST.get('education', '').strip()
            location = request.POST.get('location', '').strip()
            job_type = request.POST.get('job_type', '').strip()
            work_mode = request.POST.get('work_mode', '').strip()
            r_and_r = request.POST.get('r_and_r', '').strip()
            job_link = request.POST.get('job_link', '').strip()
            company_name = request.POST.get('company_name', '').strip()
            required_skills = request.POST.get('skills', '').strip()

            # Validation for mandatory fields
            if not job_title or not company_name or not location or not job_link:
                if not job_title:
                    messages.error(request, "Job Title is required!")
                if not company_name:
                    messages.error(request, "Company Name is required!")
                if not location:
                    messages.error(request, "Location is required!")
                if not job_link:
                    messages.error(request, "Job Link is required!")
                return redirect('add_job')  # Redirect back to the form
            
            # Create job entry in the database
            Jobs.objects.create(
                job_title=job_title,
                salary=salary,
                experience=experience,
                education=education,
                location=location,
                job_type=job_type,
                work_mode=work_mode,
                required_skills=required_skills,
                roles_and_responsibilities=r_and_r,
                jon_link=job_link,
                company_name=company_name,
                added_by=added_by,
            )
            messages.success(request, "Job added successfully!")
            return redirect('add_job')  # Redirect back to form or another page
        except Exception as e:
            # Log the error for debugging if needed
            print(e)
            messages.error(request, "Failed to add the job. Please try again.")
            return redirect('add_job')

    return render(request, 'add_job.html')

def job_details(request):
    data = Jobs.objects.all()
    context = {
        'data': data
    }
    return render(request, 'job_details.html', context)

def get_job_details(request, id):
    try:
        job = Jobs.objects.get(id=id)
        data = {
            'job_title': job.job_title,
            'company_name': job.company_name,
            'salary': job.salary,
            'experience': job.experience,
            'location': job.location,
            'education': job.education,
            'job_type': job.job_type,
            'work_mode': job.work_mode,
            'required_skills': job.required_skills,
            'roles_and_responsibilities': job.roles_and_responsibilities,
            'jon_link': job.jon_link,
        }
        return JsonResponse(data)
    except Jobs.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)
    
