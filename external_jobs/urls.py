from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('admin_db',views.admin_db,name='admin_db'),
    path('v3_login',views.v3_login,name='v3_login'),
    path('register',views.register,name='register'),
    path('admin_logout',views.admin_logout,name="admin_logout"),
    path('job_details',views.job_details,name="job_details"),
    path('add_job',views.add_job,name="add_job"),
    path('get_job_details/<int:id>/', views.get_job_details, name='get_job_details'),
    path('edit_job_details/<int:id>/', views.edit_job_details, name='edit_job_details'),
    path('delete_job/<int:id>/', views.delete_job, name='delete_job'),
    path('login',views.user_login,name='user_login'),
    path('user_registration',views.user_registration,name='user_registration'),
    path('jobs',views.jobs,name='jobs'),
    path('dashbord',views.user_dashboard,name='user_dashboard'),
    
]