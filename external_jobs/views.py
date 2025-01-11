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
    return render(request,'job_details.html')

def add_job(request):
    return render(request,'add_job.html')

def admin_logout(request):
    logout(request)
    return redirect('/admin_login')

def register(request):
    return render(request,'register.html')