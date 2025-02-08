from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from . models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.hashers import make_password
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

def admin_logout(request):
    logout(request)
    return redirect('/admin_login')

def register(request):
    return render(request,'register.html')
def add_job(request):
    alert = {"type": "", "message": ""}

    if request.method == 'POST':
        try:
            added_by = request.user
            job_title = request.POST.get('job_title')
            experience = request.POST.get('experience')
            salary = request.POST.get('package')
            education = request.POST.get('education')
            location = request.POST.get('location')
            job_type = request.POST.get('job_type')
            work_mode = request.POST.get('work_mode')
            r_and_r = request.POST.get('r_and_r')
            job_link = request.POST.get('job_link')
            company_name = request.POST.get('company_name')
            required_skills = request.POST.get('skills')
            company_logo = request.FILES.get('company_logo')  # Handle logo upload

            if not job_title or not company_name or not location :
                missing_fields = []
                if not job_title:
                    missing_fields.append("Job Title")
                if not company_name:
                    missing_fields.append("Company Name")
                if not location:
                    missing_fields.append("Location")
                

                alert["type"] = "error"
                alert["message"] = f"Missing required fields: {', '.join(missing_fields)}"
                return render(request, 'add_job.html', {"alert": alert})

            # Create job entry
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
                job_link=job_link,
                company_name=company_name,
                company_logo=company_logo,
                added_by=added_by,
            )

            
        except Exception as e:
            print(e)
            alert["type"] = "error"
            alert["message"] = "Failed to add the job. Please try again."
            return render(request, 'add_job.html', {"alert": alert})

    return render(request, 'add_job.html', {"alert": alert})


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
            'job_link': job.job_link,
        }
        return JsonResponse(data)
    except Jobs.DoesNotExist:
        return JsonResponse({'error': 'Job not found'}, status=404)


def edit_job_details(request, id):
   
    job = get_object_or_404(Jobs, id=id)

    if request.method == 'POST':
        # Retrieve data from the form
        job.job_title = request.POST.get('job_title')
        job.company_name = request.POST.get('company_name')
        job.location = request.POST.get('location')
        job.job_type = request.POST.get('job_type')
        job.job_link = request.POST.get('job_link')
        job.experience = request.POST.get('experience')
        job.salary = request.POST.get('package')
        job.work_mode = request.POST.get('work_mode')
        job.education = request.POST.get('education')
        job.required_skills = request.POST.get('skills')
        job.roles_and_responsibilities = request.POST.get('r_and_r')

        # Save updated details
        job.save()
        
        return redirect('job_details')  # Replace with your list view name

    context = {
        'data': job
    }
    return render(request, 'edit_job_details.html', context)


def delete_job(request, id):
    if request.method == 'DELETE':
        job = get_object_or_404(Jobs, id=id)
        job.delete()
        return JsonResponse({'message': 'Job deleted successfully!'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def index(request):
    latest_jobs = Jobs.objects.order_by('-id')[:5]  # Fetch the 5 most recent jobs
    return render(request, 'index.html', {'latest_jobs': latest_jobs})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username = username, password = password)
        if user is not None :
            print("inside if")
            login(request,user)
            return redirect('/dashboard')
        else:
            print("inside else")
            error_message = "Invalid username or password"
            return render(request,'user_login.html',{'error_message':error_message})
    return render(request, 'user_login.html')

def user_registration(request):
    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        encrypted_password = make_password(c_password) 
        # Validation checks
        if not full_name or not email or not phone_no or not password or not c_password:
            messages.error(request, "All fields are required!")
        elif len(phone_no) != 10 or not phone_no.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits!")
        elif password != c_password:
            messages.error(request, "Password and Confirm Password do not match!")
        else:
            # Save user if validation passes
            NewUser.objects.create(fullname=full_name, username=email, phone_no=phone_no, password=encrypted_password)
            return render(request, 'user_registration.html', {'success': True})

    return render(request, 'user_registration.html')


def jobs(request):
    job_list = Jobs.objects.all()  # Fetch all jobs from the database
    return render(request, 'jobs.html', {'jobs': job_list})



def user_dashboard(request):
    job_list = Jobs.objects.all()  # Fetch all jobs from the database
    return render(request, 'user_dashboard.html', {'jobs': job_list})