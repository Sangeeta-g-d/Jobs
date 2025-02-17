from itertools import count
from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from . models import *
from django.contrib import messages
from django.http import JsonResponse
from datetime import date, datetime
from django.contrib.auth.hashers import make_password
from django.db.models import Count

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
    total_jobs = Jobs.objects.exclude(job_link='nolink').count()  # Count jobs with valid links
    total_companies = NewUser.objects.filter(user_type='Company').count()  # Count companies

    # Get companies with the number of jobs posted
    companies = NewUser.objects.filter(user_type='Company').annotate(
        total_jobs=Count('jobs')
    )

    return render(request, 'admin_db.html', {
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'companies': companies
    })

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
            category = request.POST.get('category')
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
                category = category,
                company_name=company_name,
                company_logo=company_logo,
                added_by=added_by,
                date_posted=date.today(),
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

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')  # Redirect to dashboard after login
        else:
            error_message = "Invalid username or password"
            return render(request, 'user_login.html', {'error_message': error_message})

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
    selected_location = request.GET.get('location')
    selected_category = request.GET.get('category')
    selected_job_type = request.GET.get('job_type')

    # Store filters in session
    request.session['selected_location'] = selected_location
    request.session['selected_category'] = selected_category
    request.session['selected_job_type'] = selected_job_type

    # Fetch unique values for filters
    unique_locations = Jobs.objects.values_list('location', flat=True).distinct()
    unique_categories = Jobs.objects.values_list('category', flat=True).distinct()
    unique_job_types = Jobs.objects.values_list('job_type', flat=True).distinct()

    # Apply filters
    job_list = Jobs.objects.all()
    if selected_location:
        job_list = job_list.filter(location=selected_location)
    if selected_category:
        job_list = job_list.filter(category=selected_category)
    if selected_job_type:
        job_list = job_list.filter(job_type=selected_job_type)

    return render(request, 'jobs.html', {
        'jobs': job_list,
        'locations': unique_locations,
        'categories': unique_categories,
        'job_types': unique_job_types,
        'selected_location': selected_location,
        'selected_category': selected_category,
        'selected_job_type': selected_job_type
    })
from datetime import timedelta, date

def user_dashboard(request):
    # Get filters from GET parameters or session
    selected_location = request.GET.get('location', request.session.get('selected_location'))
    selected_category = request.GET.get('category', request.session.get('selected_category'))
    selected_job_type = request.GET.get('job_type', request.session.get('selected_job_type'))
    selected_work_mode = request.GET.get('work_mode', request.session.get('selected_work_mode'))
    selected_experience = request.GET.get('experience', request.session.get('selected_experience'))
    selected_date_posted = request.GET.get('date_posted', request.session.get('selected_date_posted'))
    search_query = request.GET.get('search', '')

    # Update session values if new filters are applied
    if request.GET.get('location') is not None:
        request.session['selected_location'] = selected_location
    if request.GET.get('category') is not None:
        request.session['selected_category'] = selected_category
    if request.GET.get('job_type') is not None:
        request.session['selected_job_type'] = selected_job_type
    if request.GET.get('work_mode') is not None:
        request.session['selected_work_mode'] = selected_work_mode
    if request.GET.get('experience') is not None:
        request.session['selected_experience'] = selected_experience
    if request.GET.get('date_posted') is not None:
        request.session['selected_date_posted'] = selected_date_posted

    # Fetch unique values for filters
    unique_locations = Jobs.objects.values_list('location', flat=True).distinct()
    unique_categories = Jobs.objects.values_list('category', flat=True).distinct()
    unique_job_types = Jobs.objects.values_list('job_type', flat=True).distinct()
    unique_work_modes = Jobs.objects.values_list('work_mode', flat=True).distinct()
    unique_experience_levels = Jobs.objects.values_list('experience', flat=True).distinct()

    # Apply filters
    job_list = Jobs.objects.all()

    if selected_location:
        job_list = job_list.filter(location=selected_location)
    if selected_category:
        job_list = job_list.filter(category=selected_category)
    if selected_job_type:
        job_list = job_list.filter(job_type=selected_job_type)
    if selected_work_mode:
        job_list = job_list.filter(work_mode=selected_work_mode)
    if selected_experience:
        job_list = job_list.filter(experience=selected_experience)
    if search_query:
        job_list = job_list.filter(job_title__icontains=search_query)

    # Date Posted Filter
    if selected_date_posted:
        today = date.today()
        if selected_date_posted == "1_day":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=1))
        elif selected_date_posted == "3_days":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=3))
        elif selected_date_posted == "1_week":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=7))

    return render(request, 'user_dashboard.html', {
        'jobs': job_list,
        'locations': unique_locations,
        'categories': unique_categories,
        'job_types': unique_job_types,
        'work_modes': unique_work_modes,
        'experience_levels': unique_experience_levels,
        'selected_location': selected_location,
        'selected_category': selected_category,
        'selected_job_type': selected_job_type,
        'selected_work_mode': selected_work_mode,
        'selected_experience': selected_experience,
        'selected_date_posted': selected_date_posted,
        'search_query': search_query
    })



def company_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('username')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        image = request.FILES.get('profile_image')  # Handle uploaded image
        print(full_name,email,phone_no,address,password,c_password)
        encrypted_password = make_password(password)

        # Validation checks
        if not full_name or not email  or not password or not c_password or not address:
            messages.error(request, "All fields are required!")
        elif len(phone_no) != 10 or not phone_no.isdigit():
            messages.error(request, "Phone number must be exactly 10 digits!")
        elif password != c_password:
            messages.error(request, "Password and Confirm Password do not match!")
        else:
            # Save user if validation passes
            NewUser.objects.create(
                fullname=full_name,
                username=email,
                phone_no=phone_no,
                address=address,
                password=encrypted_password,
                profile_image=image,
                user_type = 'Company'
            )
            return render(request, 'company_register.html', {'success': True})

    
    return render(request, 'company_register.html')


def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:  # Check if the admin has approved the user
                login(request, user)
                return redirect('/company_db')
            else:
                print(user.is_staff)
                error_message = "Admin has not approved your account yet."
        else:
            error_message = "Invalid username or password."
        return render(request, 'company_login.html', {'error_message': error_message})
    return render(request, 'company_login.html')


def company_list(request):
    data = NewUser.objects.filter(user_type='Company').all()
    return render(request, 'company_list.html', {'data': data})

def toggle_approval(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(NewUser, id=user_id)
        user.is_staff = not user.is_staff  # Toggle the approval status
        user.save()
        return JsonResponse({"success": True, "is_staff": user.is_staff})
    return JsonResponse({"success": False})


def company_db(request):
    return render(request, 'company_db.html')


def company_base(request):
    return render(request, 'company_base.html')

def company_add_job(request):
    alert = {"type": "", "message": ""}
    user = request.user.id
    data = NewUser.objects.filter(id=user).first()  # Fetch single user instance
    
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
            
            company_name = request.POST.get('company_name')
            category = request.POST.get('category')
            required_skills = request.POST.get('skills')
            company_logo = request.FILES.get('company_logo', data.profile_image if data else None)  # Use profile_image if no new upload

            if not job_title or not company_name or not location:
                missing_fields = [field for field, value in [("Job Title", job_title), ("Company Name", company_name), ("Location", location)] if not value]
                
                alert["type"] = "error"
                alert["message"] = f"Missing required fields: {', '.join(missing_fields)}"
                return render(request, 'company_add_job.html', {"alert": alert, "data": data})
            
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
                
                category=category,
                company_name=company_name,
                company_logo=company_logo,
                added_by=added_by,
                date_posted=date.today(),
            )

            alert["type"] = "success"
            alert["message"] = "Job posted successfully!"
        except Exception as e:
            print(e)
            alert["type"] = "error"
            alert["message"] = "Failed to add the job. Please try again."

    return render(request, 'company_add_job.html', {"alert": alert, "data": data})

def get_user_details(request):
    user = request.user
    return JsonResponse({
        "username": user.fullname,
        "phone": user.phone_no,
        "email": user.username
    })
def apply_job(request):
    if request.method == "POST":
        user = request.user
        job_id = request.POST.get("job_id")
        resume = request.FILES.get("resume")

        if not job_id or not resume:
            return JsonResponse({"message": "Invalid request!"}, status=400)

        try:
            job = Jobs.objects.get(id=job_id)
            print("FFFFFFF",job, job.added_by_id)
        except Jobs.DoesNotExist:
            return JsonResponse({"message": "Job not found!"}, status=404)

        # Assuming Jobs model has a ForeignKey to Company model
        AppliedJob.objects.create(user=user, job_id=job_id, resume=resume, company=job.added_by_id)

        return JsonResponse({"message": "Your application has been submitted successfully!"})

    return JsonResponse({"message": "Invalid request!"}, status=400)

def company_job_details(request):
    company_id = request.user.id
    data = Jobs.objects.filter(added_by_id=company_id, status="Active")  # Fetch only active jobs
    context = {
        'data': data
    }
    return render(request, 'company_job_details.html', context)


def toggle_job_status(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)

    # Change the status
    if job.status == "Active":
        job.status = "Inactive"
    else:
        job.status = "Active"
    
    job.save()
    return JsonResponse({"success": True, "new_status": job.status})

def company_edit_job_details(request, id):
   
    job = get_object_or_404(Jobs, id=id)

    if request.method == 'POST':
        # Retrieve data from the form
        job.job_title = request.POST.get('job_title')
        job.company_name = request.POST.get('company_name')
        job.location = request.POST.get('location')
        job.job_type = request.POST.get('job_type')
        job.experience = request.POST.get('experience')
        job.salary = request.POST.get('package')
        job.work_mode = request.POST.get('work_mode')
        job.education = request.POST.get('education')
        job.required_skills = request.POST.get('skills')
        job.roles_and_responsibilities = request.POST.get('r_and_r')

        # Save updated details
        job.save()
        
        return redirect('company_job_details')  # Replace with your list view name

    context = {
        'data': job
    }
    return render(request, 'company_edit_job_details.html', context)

def company_applied_jobs(request):
    company_id = request.user.id
    jobs = Jobs.objects.filter(added_by=company_id)  # Filter jobs by the logged-in company
    return render(request, 'company_applied_jobs.html', {'jobs': jobs})


def c_applied_candidates(request, job_id):
    # Get the applied candidates for the given job_id
    applied_candidates = AppliedJob.objects.filter(job_id=job_id)

    # Fetch user details for each application
    candidate_details = []
    for application in applied_candidates:
        user = get_object_or_404(NewUser, id=application.user.id)
        candidate_details.append({
            'fullname': user.fullname,
            'email': user.username,
            'phone_no': user.phone_no,
            'resume': application.resume.url if application.resume else None,
            'applied_at': application.applied_at,
        })

    context = {
        'candidate_details': candidate_details
    }
    return render(request, 'c_applied_candidates.html', context)

def a_company_jobs(request,id):
    print(id)
    c_name = Jobs.objects.filter(added_by_id=id).first()
    jobs= Jobs.objects.filter(added_by_id= id)
    context = {
        'jobs': jobs,
        'c_name':c_name
    }
    return render(request,'a_company_jobs.html',context)


def a_candidate_details(request,id):
    applied_candidates = AppliedJob.objects.filter(job_id=id)
    print(applied_candidates)
    # Fetch user details for each application
    candidate_details = []
    for application in applied_candidates:
        user = get_object_or_404(NewUser, id=application.user.id)
        print(user.fullname)
        candidate_details.append({
            'fullname': user.fullname,
            'email': user.username,
            'phone_no': user.phone_no,
            'resume': application.resume.url if application.resume else None,
            'applied_at': application.applied_at,
        })
    context = {
        'candidate_details': candidate_details
        }

    return render(request,'a_candidate_details.html',context)