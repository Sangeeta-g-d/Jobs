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
from datetime import timedelta, date
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
# forgot password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings


User = get_user_model()
# Create your views here.

# forgot password
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            token = default_token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(reverse('reset_password', args=[uidb64, token]))

            # Professional Email Content
            subject = "Password Reset Request - JobTriad"
            message = f"""
            Dear {user.first_name},

            We received a request to reset your password for your JobTriad account. If you did not request this, please ignore this email.

            To reset your password, please click the link below:
            {reset_link}

            If the above link does not work, copy and paste it into your browser's address bar.

            If you need further assistance, please contact our support team.

            Best regards,  
            JobTriad Team  
            jobtriad@gmail.com  
            """

            # Send email
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )

            return render(request, 'password_reset_sent.html')

        return render(request, 'forgot_password.html', {'error': 'No user found with this email.'})

    return render(request, 'forgot_password.html')



def password_reset_sent(request):
    return render(request,'password_reset_sent.html')

def password_reset_success(request):
    return render(request,'password_reset_success.html')

# Reset password - Form submission
def reset_password(request, uidb64, token):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Passwords do not match.', 'uidb64': uidb64, 'token': token})

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            return render(request, 'reset_password.html', {'error': 'Invalid reset link.'})

        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()

            # Store user type in session
            request.session['user_type'] = user.user_type if hasattr(user, 'user_type') else None

            return redirect('password_reset_success')  # Redirect to success page

    return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})

def admin_logout(request):
    logout(request)
    return redirect('/v3_login')

def company_logout(request):
    logout(request)
    return redirect('/company_login')

def user_logout(request):
    logout(request)
    return redirect('/')


def v3_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(username = username, password = password)
        print(user)
        if user is not None and user.is_superuser == True:
            login(request,user)
            return redirect('/admin_db')
        else:
            error_message = "Invalid username or password"
            return render(request,'v3_login.html',{'error_message':error_message})
    return render(request,'v3_login.html')

@login_required
def admin_db(request):
    total_jobs = Jobs.objects.exclude(job_link='nolink').count()  # Count jobs with valid links
    total_companies = NewUser.objects.filter(user_type='Company').count()  # Count companies
    username= request.user.username
    print(username)
    # Get companies with the number of jobs posted
    companies = NewUser.objects.filter(user_type='Company').annotate(
        total_jobs=Count('jobs')
    )

    return render(request, 'admin_db.html', {
        'total_jobs': total_jobs,
        'total_companies': total_companies,
        'companies': companies,
        'username':username
    })

def register(request):
    return render(request,'register.html')

@login_required
def add_job(request):
    alert = {"type": "", "message": ""}
    username= request.user.username
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

    return render(request, 'add_job.html', {"alert": alert,'username':username})

@login_required
def job_details(request):
    id= request.user.id
    data = Jobs.objects.filter(added_by_id=id)
    username= request.user.username
    context = {
        'data': data,
        'username':username
    }
    return render(request, 'job_details.html', context)

@login_required
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

@login_required
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

@login_required
def delete_job(request, id):
    print(id,"idddddddd")
    job = get_object_or_404(Jobs, id=id, added_by=request.user)
    
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('company_job_details')  # Redirect back to job listing page

@login_required
def delete_job_admin(request, id):
    print(id, "idddddddd")
    job = get_object_or_404(Jobs, id=id)  # Removed `added_by=request.user`
    
    if request.method == "POST":
        job.delete()
        messages.success(request, "Job deleted successfully.")
        return redirect('job_details')  # Redirect to job listing page


def index(request):
    latest_jobs = Jobs.objects.order_by('-id')[:5]
    
    # Count jobs for each category
    DC = Jobs.objects.filter(category="Design-Creative").count()
    Marketing = Jobs.objects.filter(category="Marketing").count()
    TM = Jobs.objects.filter(category="Telemarketing").count()
    SW = Jobs.objects.filter(category="Software and Web").count()
    administration = Jobs.objects.filter(category="Administration").count()
    TE = Jobs.objects.filter(category="Teaching and Education").count()
    engineering = Jobs.objects.filter(category="Engineering (Hardware)").count()
    healthcare = Jobs.objects.filter(category="Healthcare").count()
    
    context = {
        'DC': DC,
        'Marketing': Marketing,
        'TM': TM,
        'SW': SW,
        'administration': administration,
        'TE': TE,
        'engineering': engineering,
        'healthcare': healthcare,
        'latest_jobs': latest_jobs
    }
    return render(request, 'index.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        #print(username, password)
        user = authenticate(username=username, password=password)
        print("++++++++++++",user)
        if user is not None:
            login(request, user)
            return redirect('/dashboard')  # Redirect to dashboard after login
        else:
            error_message = "Invalid username or password"
            return render(request, 'user_login.html', {'error_message': error_message})

    return render(request, 'user_login.html')


def check_email(request):
    email = request.GET.get('email')
    print(email)
    if NewUser.objects.filter(username=email).exists():
        return JsonResponse({'exists': True})
    return JsonResponse({'exists': False})

def user_registration(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        phone = request.POST['phone_no']
        email = request.POST['email']
        password = request.POST['password']
        encrypted_password = make_password(password) 


        if NewUser.objects.filter(username=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists!'})

        # Save User
        user = NewUser.objects.create_user(username=email, phone_no=phone,  fullname=fullname, email=email)
        user.set_password(password)  # Hash password properly
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Registration Successful!'})

    return render(request, 'user_registration.html')


def jobs(request):
    if request.GET.get('reset'):
        request.session.pop('searched_jobs', None)
        request.session.pop('filters', None)  # Clear filters
        return redirect('jobs')
    # Get user search input
    search_query = request.GET.get('search', '').strip()
    selected_designation = request.GET.get('designation', '').strip()
    print("----------------------",selected_designation)
    selected_location = request.GET.get('location', '').strip()
    selected_category = request.GET.get('category', '').strip()
    selected_job_type = request.GET.get('job_type', '').strip()
    selected_work_mode = request.GET.get('work_mode', '').strip()
    selected_experience = request.GET.get('experience', '').strip()
    selected_date_posted = request.GET.get('date_posted', '').strip()

    request.session['filters'] = {
        'search_query': search_query,
        'designation': selected_designation,
        'location': selected_location,
        'category': selected_category,
        'job_type': selected_job_type,
        'work_mode': selected_work_mode,
        'experience': selected_experience,
        'date_posted': selected_date_posted,
    }

    # Fetch unique filters for the dropdowns
    unique_locations = Jobs.objects.values_list('location', flat=True).distinct()
    unique_categories = Jobs.objects.values_list('category', flat=True).distinct()
    unique_job_types = Jobs.objects.values_list('job_type', flat=True).distinct()
    unique_work_modes = Jobs.objects.values_list('work_mode', flat=True).distinct()
    unique_experience_levels = Jobs.objects.values_list('experience', flat=True).distinct()


    # If a new search is made, store the job IDs in the session
    if search_query:
        job_list = Jobs.objects.filter(job_title__icontains=search_query)
        request.session['searched_jobs'] = list(job_list.values_list('id', flat=True))
    else:
        searched_job_ids = request.session.get('searched_jobs', [])
        job_list = Jobs.objects.filter(id__in=searched_job_ids) if searched_job_ids else Jobs.objects.all()

    # Apply filters only to the searched results
    if selected_designation:
        job_list = job_list.filter(job_title__icontains=selected_designation)
        request.session['searched_jobs'] = list(job_list.values_list('id', flat=True))
    else:
        searched_job_ids = request.session.get('searched_jobs', [])
        job_list = Jobs.objects.filter(id__in=searched_job_ids) if searched_job_ids else Jobs.objects.all()

    if selected_location:
        job_list = job_list.filter(location__icontains=selected_location)

    if selected_category:
        job_list = job_list.filter(category__icontains=selected_category)

    if selected_job_type:
        job_list = job_list.filter(job_type__icontains=selected_job_type)

    if selected_work_mode:
        job_list = job_list.filter(work_mode=selected_work_mode)

    if selected_experience:
        job_list = job_list.filter(experience=selected_experience)

    if selected_date_posted:
        today = date.today()
        if selected_date_posted == "1_day":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=1))
        elif selected_date_posted == "3_days":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=3))
        elif selected_date_posted == "1_week":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=7))

    # Compute job age (days since posted)
    jobs_with_age = [{'job': job, 'days_old': (now().date() - job.date_posted).days} for job in job_list]

    context = {
        'jobs_with_age': jobs_with_age,
        'locations': unique_locations,
        'categories': unique_categories,
        'job_types': unique_job_types,
        'work_modes': unique_work_modes,
        'experience_levels': unique_experience_levels,
        'selected_location': selected_location,
        'selected_designation': selected_designation,
        'selected_category': selected_category,
        'selected_job_type': selected_job_type,
        'search_query': search_query,  # Persist search query
    }

    return render(request, 'jobs.html', context)


@login_required
def user_dashboard(request):
    if request.GET.get('reset'):
        keys_to_clear = [
        'selected_location', 'selected_category', 'selected_job_type', 
        'selected_work_mode', 'selected_experience', 'selected_date_posted', 
        'search_query', 'designation', 'searched_jobs'
        ]
        for key in keys_to_clear:
            request.session.pop(key, None)  # Remove key if it exists
        return redirect('user_dashboard')  # Redirect to clear URL params
    # Check if session has saved filters from pre-login state
    selected_location = request.GET.get('location', request.session.get('selected_location', ''))
    selected_category = request.GET.get('category', request.session.get('selected_category', ''))
    selected_job_type = request.GET.get('job_type', request.session.get('selected_job_type', ''))
    selected_work_mode = request.GET.get('work_mode', request.session.get('selected_work_mode', ''))
    selected_experience = request.GET.get('experience', request.session.get('selected_experience', ''))
    selected_date_posted = request.GET.get('date_posted', request.session.get('selected_date_posted', ''))
    search_query = request.GET.get('search', request.session.get('search_query', ''))
    selected_designation = request.GET.get('designation', request.session.get('designation', ''))

    # Store new filters in session
    if request.GET:
        request.session['selected_location'] = selected_location
        request.session['selected_category'] = selected_category
        request.session['selected_job_type'] = selected_job_type
        request.session['selected_work_mode'] = selected_work_mode
        request.session['selected_experience'] = selected_experience
        request.session['selected_date_posted'] = selected_date_posted
        request.session['search_query'] = search_query
        request.session['designation'] = selected_designation
    
    print("***************************",selected_designation)
    # Fetch unique values for dropdown filters
    unique_locations = Jobs.objects.values_list('location', flat=True).distinct()
    unique_categories = Jobs.objects.values_list('category', flat=True).distinct()
    unique_job_types = Jobs.objects.values_list('job_type', flat=True).distinct()
    unique_work_modes = Jobs.objects.values_list('work_mode', flat=True).distinct()
    unique_experience_levels = Jobs.objects.values_list('experience', flat=True).distinct()

    # Apply filters
    job_list = Jobs.objects.all()

    if search_query:
        job_list = Jobs.objects.filter(job_title__icontains=search_query)
        request.session['searched_jobs'] = list(job_list.values_list('id', flat=True))
    else:
        searched_job_ids = request.session.get('searched_jobs', [])
        job_list = Jobs.objects.filter(id__in=searched_job_ids) if searched_job_ids else Jobs.objects.all()

    # Apply filters only to the searched results
    if selected_designation:
        job_list = job_list.filter(job_title__icontains=selected_designation)
        request.session['searched_jobs'] = list(job_list.values_list('id', flat=True))
    else:
        searched_job_ids = request.session.get('searched_jobs', [])
        job_list = Jobs.objects.filter(id__in=searched_job_ids) if searched_job_ids else Jobs.objects.all()

    if selected_location:
        job_list = job_list.filter(location__icontains=selected_location)
    if selected_category:
        job_list = job_list.filter(category__icontains=selected_category)
    if selected_job_type:
        job_list = job_list.filter(job_type__icontains=selected_job_type)
    if selected_work_mode:
        job_list = job_list.filter(work_mode=selected_work_mode)
    if selected_experience:
        job_list = job_list.filter(experience=selected_experience)
    

    # Date Posted Filter
    if selected_date_posted:
        today = date.today()
        if selected_date_posted == "1_day":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=1))
        elif selected_date_posted == "3_days":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=3))
        elif selected_date_posted == "1_week":
            job_list = job_list.filter(date_posted__gte=today - timedelta(days=7))

    jobs_with_age = [{'job': job, 'days_old': (now().date() - job.date_posted).days} for job in job_list]

    return render(request, 'user_dashboard.html', {
        'jobs_with_age':jobs_with_age,
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

def check_username(request):
    username = request.GET.get('username')
    exists = NewUser.objects.filter(fullname=username).exists()
    return JsonResponse({'exists': exists})

def company_register(request):
    if request.method == 'POST':
        full_name = request.POST.get('username')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        password = request.POST.get('password')
        c_password = request.POST.get('c_password')
        image = request.FILES.get('profile_image')  # Handle uploaded image

        # Validate required fields
        if not all([full_name, email, phone_no, address, password, c_password]):
            return JsonResponse({'status': 'error', 'message': 'All fields are required!'})

        # Check if email already exists
        if NewUser.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists!'})
        
        # Check if username (company name) already exists
        if NewUser.objects.filter(fullname=full_name).exists():
            return JsonResponse({'status': 'error', 'message': 'Company name already exists!'})

       
        # Encrypt password
        encrypted_password = make_password(password)

        # Create and save user
        user = NewUser.objects.create_user(
            fullname=full_name,
            username=email,  # Using email as username
            phone_no=phone_no,
            address=address,
            profile_image=image,
            user_type='Company',
            email=email
        )
        user.set_password(password)  # Hash password properly
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Company Registration Successful!'})

    return render(request, 'company_register.html')


def company_login(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            print("user")
            if user.is_staff:
                login(request, user)
                return redirect('/company_db')
            else:
                error_message = "Admin has not approved your account yet."
        else:
            error_message = "Invalid username or password."
        
        return render(request, 'company_login.html', {'error_message': error_message})
    
    return render(request, 'company_login.html')

@login_required
def company_list(request):
    data = NewUser.objects.filter(user_type='Company').all()
    username= request.user.username
    return render(request, 'company_list.html', {'data': data,'username':username})

@login_required
def toggle_approval(request, user_id):
    if request.method == "POST":
        user = get_object_or_404(NewUser, id=user_id)
        user.is_staff = not user.is_staff  # Toggle the approval status
        user.save()
        return JsonResponse({"success": True, "is_staff": user.is_staff})
    return JsonResponse({"success": False})

@login_required
def company_db(request):
    user = request.user
    username = user.fullname
    logo = user.profile_image

    # Count total jobs added by the company
    total_jobs = Jobs.objects.filter(added_by=user).count()

    # Count total applicants for all jobs posted by the company
    job_ids = Jobs.objects.filter(added_by=user).values_list('id', flat=True)
    total_applicants = AppliedJob.objects.filter(job_id__in=job_ids).count()
    print(total_applicants,"gggggggggggg")
    # Get all jobs added by the company
    jobs = Jobs.objects.filter(added_by=user)

    return render(request, 'company_db.html', {
        'username': username,
        'logo': logo,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'jobs': jobs,
    })

def company_base(request):
    return render(request, 'company_base.html')

@login_required
def company_add_job(request):
    alert = {"type": "", "message": ""}
    user = request.user.id
    username= request.user.fullname
    logo=request.user.profile_image
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

    return render(request, 'company_add_job.html', {"alert": alert, "data": data,'username':username,'logo':logo})

@login_required
def get_user_details(request):
    user = request.user
    return JsonResponse({
        "username": user.fullname,
        "phone": user.phone_no,
        "email": user.username
    })

@login_required
def apply_job(request):
    if request.method == "POST":
        user = request.user
        job_id = request.POST.get("job_id")
        resume = request.FILES.get("resume")

        if not job_id or not resume:
            return JsonResponse({"message": "Invalid request!"}, status=400)

        try:
            job = Jobs.objects.get(id=job_id)
            print("FFFFFFF", job, job.added_by_id)
        except Jobs.DoesNotExist:
            return JsonResponse({"message": "Job not found!"}, status=404)

        # Use the job instance instead of job_id
        AppliedJob.objects.create(user=user, job_id=job, resume=resume, company=job.added_by_id)

        return JsonResponse({"message": "Your application has been submitted successfully!"})

    return JsonResponse({"message": "Invalid request!"}, status=400)


@login_required
def company_job_details(request):
    company_id = request.user.id
    username = request.user.fullname
    logo = request.user.profile_image
    search_query = request.GET.get('search', '').strip()  # Get search query

    data = Jobs.objects.filter(added_by_id=company_id, status="Active")  

    if search_query:
        data = data.filter(job_title__icontains=search_query)  # Filter by job title

    context = {
        'data': data,
        'username': username,
        'logo': logo,
        'search_query': search_query
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

@login_required
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

@login_required
def company_applied_jobs(request):
    company_id = request.user.id
    username = request.user.fullname
    logo = request.user.profile_image
    search_query = request.GET.get('search', '')  # Get search query from the request

    # Filter jobs by the logged-in company and search for job title if query is provided
    if search_query:
        jobs = Jobs.objects.filter(added_by=company_id, job_title__icontains=search_query)
    else:
        jobs = Jobs.objects.filter(added_by=company_id)

    return render(request, 'company_applied_jobs.html', {'jobs': jobs, 'username': username, 'logo': logo, 'search_query': search_query})


@login_required
def c_applied_candidates(request, job_id):
    username= request.user.fullname
    logo=request.user.profile_image
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
        'candidate_details': candidate_details,
        'username':username,
        'logo':logo
    }
    return render(request, 'c_applied_candidates.html', context)

@login_required
def a_company_jobs(request,id):
    print(id)
    c_name = Jobs.objects.filter(added_by_id=id).first()
    jobs= Jobs.objects.filter(added_by_id= id)
    username= request.user.username
    context = {
        'jobs': jobs,
        'c_name':c_name,
        'username':username
    }
    return render(request,'a_company_jobs.html',context)

@login_required
def a_candidate_details(request,id):
    applied_candidates = AppliedJob.objects.filter(job_id=id)
    username= request.user.username
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
        'candidate_details': candidate_details,
        'username':username
        }

    return render(request,'a_candidate_details.html',context)

@login_required
def company_inactive_job(request):
    company_id = request.user.id
    username= request.user.fullname
    logo=request.user.profile_image
    data = Jobs.objects.filter(added_by_id=company_id, status="Inactive")  # Fetch only active jobs
    context = {
        'data': data,
        'username':username,
        'logo':logo
    }
    return render(request, 'company_inactive_jobs.html', context)

@login_required
def toggle_job_status_inactive(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)

    # Change the status
    if job.status == "Inactive":
        job.status = "Active"
    else:
        job.status = "Inactive"
    
    job.save()
    return JsonResponse({"success": True, "new_status": job.status})

@login_required
def user_applied_jobs(request):
    user_id = request.user.id
    search_query = request.GET.get('search', '').strip()  # Get the search query from the request

    # Fetch all applied jobs of the logged-in user
    applied_jobs = AppliedJob.objects.filter(user_id=user_id).select_related('user')

    # Filter jobs by company name if search query is provided
    job_details = []
    for applied_job in applied_jobs:
        job = Jobs.objects.get(id=applied_job.job_id_id)
        if search_query.lower() in job.company_name.lower():  # Case-insensitive search
            job_details.append({
                'company_logo': job.company_logo.url if job.company_logo else None,
                'company_name': job.company_name,
                'job_title': job.job_title,
                'applied_at': applied_job.applied_at.strftime('%d-%m-%Y'),
                'resume': applied_job.resume.url,
                'job_id': job.id
            })

    return render(request, 'user_applied_jobs.html', {'job_details': job_details, 'search_query': search_query})

@login_required
def u_applied_job_detail(request, job_id):
    job = get_object_or_404(Jobs, id=job_id)
    return render(request, 'u_applied_job_detail.html', {'job': job})


def about_us(request):
    return render(request, 'about_us.html')

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        message = request.POST.get('message')
        
        if name and email and phone_no and message:
            Contact_us.objects.create(name=name, email=email, phone_no=phone_no, message=message)
            return JsonResponse({'message': 'Form submitted successfully!'})
        else:
            return JsonResponse({'message': 'Please fill in all fields!'})

    return render(request, 'contact_us.html')

@login_required
def contact_us_details(request):
    data = Contact_us.objects.all()
    username= request.user.username
    return render(request, 'contact_us_details.html', {'data': data,'username':username})

from django.shortcuts import redirect

@login_required
def user_profile(request):
    user_details, created = UserDetails.objects.get_or_create(user_id=request.user)
    saved = False
    
    if request.method == 'POST':
        user = request.user

        # Update user's basic info
        user.fullname = request.POST.get('fullname', '').strip()
        user.phone_no = request.POST.get('phone_no', '').strip()
        user.email = request.POST.get('email', '').strip()  # Keep email separate from username

        if 'profile' in request.FILES:
            user.profile_image = request.FILES['profile']
        
        user.save()  # Save the user model first

        # Update user details
        user_details.qualification = request.POST.get('qualification', '').strip()
        user_details.area_of_interest = request.POST.get('area_of_interest', '').strip()
        user_details.skills = request.POST.get('skills', '').strip()

        # Validate year_of_passing and year_of_exp
        year_of_passing = request.POST.get('year_of_passing', '').strip()
        year_of_exp = request.POST.get('year_of_exp', '').strip()

        if year_of_passing.isdigit() and len(year_of_passing) == 4:
            user_details.year_of_passing = year_of_passing
        else:
            user_details.year_of_passing = ''

        if year_of_exp.isdigit() and 0 <= int(year_of_exp) <= 50:  # Assuming valid experience range
            user_details.year_of_exp = year_of_exp
        else:
            user_details.year_of_exp = ''

        if 'resume' in request.FILES:
            user_details.user_resume = request.FILES['resume']

        user_details.save()  # Save the user details
        saved = True

    context = {'user_details': user_details, 'saved': saved}
    return render(request, 'user_profile.html', context)

@login_required
def company_profile(request):
    username= request.user.fullname
    logo=request.user.profile_image
    user = request.user  # Get the logged-in user

    if request.method == "POST":
        user.fullname = request.POST.get('fullname', user.fullname)
        user.phone_no = request.POST.get('phone_no', user.phone_no)
        user.address = request.POST.get('address', user.address)
        user.username = request.POST.get('email', user.email)
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('company_profile')

    return render(request, 'company_profile.html', {'user': user,'username':username,'logo':logo})